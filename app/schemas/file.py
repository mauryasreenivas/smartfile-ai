from typing import Any

from pydantic import BaseModel, Field


class FileMetadata(BaseModel):
    original_filename: str
    stored_filename: str
    extension: str
    content_type: str | None
    size_bytes: int
    size_mb: float


class CsvInspection(BaseModel):
    file_type: str = "csv"
    row_count: int
    column_count: int
    columns: list[str]
    preview: list[dict[str, Any]]


class ExcelSheetInspection(BaseModel):
    sheet_name: str
    estimated_row_count: int
    estimated_column_count: int
    columns: list[str]
    preview: list[dict[str, Any]]


class ExcelInspection(BaseModel):
    file_type: str = "xlsx"
    sheet_count: int
    sheets: list[ExcelSheetInspection]


class FileUploadResponse(BaseModel):
    message: str
    metadata: FileMetadata
    inspection: CsvInspection | ExcelInspection


class FileErrorResponse(BaseModel):
    detail: str = Field(examples=["Unsupported file type"])
