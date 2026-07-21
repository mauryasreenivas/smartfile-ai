from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import UploadFile

from app.core.config import Settings
from app.core.exceptions import EmptyFileError, FileTooLargeError


class FileStorageService:
    chunk_size = 1024 * 1024

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def save_upload(self, upload: UploadFile, extension: str) -> tuple[Path, int]:
        self.settings.upload_directory.mkdir(parents=True, exist_ok=True)

        stored_filename = f"{uuid4().hex}{extension}"
        destination = self.settings.upload_directory / stored_filename

        total_size = 0

        try:
            async with aiofiles.open(destination, "wb") as output_file:
                while chunk := await upload.read(self.chunk_size):
                    total_size += len(chunk)

                    if total_size > self.settings.max_upload_size_bytes:
                        raise FileTooLargeError(
                            f"File exceeds the maximum size of "
                            f"{self.settings.max_upload_size_mb} MB."
                        )

                    await output_file.write(chunk)

            if total_size == 0:
                raise EmptyFileError("The uploaded file is empty.")

            return destination, total_size

        except Exception:
            destination.unlink(missing_ok=True)
            raise

        finally:
            await upload.close()
