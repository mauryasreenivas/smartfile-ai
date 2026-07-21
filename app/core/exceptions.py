class FileProcessingError(Exception):
    """Base exception for file-processing failures."""


class UnsupportedFileTypeError(FileProcessingError):
    """Raised when the uploaded file type is not supported."""


class FileTooLargeError(FileProcessingError):
    """Raised when the uploaded file exceeds the configured size limit."""


class EmptyFileError(FileProcessingError):
    """Raised when the uploaded file is empty."""


class InvalidFileError(FileProcessingError):
    """Raised when the file cannot be parsed or inspected."""
