from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import get_settings
from app.core.exceptions import (
    EmptyFileError,
    FileTooLargeError,
    InvalidFileError,
    UnsupportedFileTypeError,
)
from app.schemas.file import FileMetadata, FileUploadResponse
from app.services.file_inspector import FileInspectorService
from app.services.file_storage import FileStorageService

router: APIRouter = APIRouter(
    prefix="/files",
    tags=["files"],
)


def validate_extension(filename: str | None) -> str:
    """Validate the uploaded file extension."""

    if not filename:
        raise UnsupportedFileTypeError(
            "The uploaded file must have a filename."
        )

    extension = Path(filename).suffix.lower()
    settings = get_settings()

    if extension not in settings.allowed_extensions:
        allowed = ", ".join(sorted(settings.allowed_extensions))

        raise UnsupportedFileTypeError(
            f"Unsupported file type '{extension or 'unknown'}'. "
            f"Allowed types: {allowed}."
        )

    return extension


@router.post(
    "/upload",
    response_model=FileUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(
    file: Annotated[UploadFile, File()],
) -> FileUploadResponse:
    """Upload, store, and inspect a CSV or Excel file."""

    settings = get_settings()

    try:
        extension = validate_extension(file.filename)

        storage_service = FileStorageService(settings)
        inspector_service = FileInspectorService(
            preview_rows=settings.preview_rows
        )

        stored_path, size_bytes = await storage_service.save_upload(
            upload=file,
            extension=extension,
        )

        try:
            inspection = inspector_service.inspect(stored_path)
        except Exception:
            stored_path.unlink(missing_ok=True)
            raise

        metadata = FileMetadata(
            original_filename=file.filename or "unknown",
            stored_filename=stored_path.name,
            extension=extension,
            content_type=file.content_type,
            size_bytes=size_bytes,
            size_mb=round(size_bytes / (1024 * 1024), 4),
        )

        return FileUploadResponse(
            message="File uploaded and inspected successfully.",
            metadata=metadata,
            inspection=inspection,
        )

    except UnsupportedFileTypeError as exc:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=str(exc),
        ) from exc

    except FileTooLargeError as exc:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(exc),
        ) from exc

    except EmptyFileError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except InvalidFileError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    finally:
        await file.close()