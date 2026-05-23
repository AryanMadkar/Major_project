from pathlib import Path

from flask import Request

from app.core.config import (
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB
)

# ======================================================
# EXTENSION VALIDATION
# ======================================================

def validate_extension(filename):

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )

# ======================================================
# FILE SIZE VALIDATION
# ======================================================

def validate_file_size(file):

    file.seek(0, 2)

    size_mb = file.tell() / (1024 * 1024)

    file.seek(0)

    if size_mb > MAX_FILE_SIZE_MB:

        raise ValueError(
            f"File exceeds {MAX_FILE_SIZE_MB}MB"
        )