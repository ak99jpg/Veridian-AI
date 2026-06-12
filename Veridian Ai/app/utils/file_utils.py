import os
import shutil
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException

async def validate_pdf(file: UploadFile) -> bool:
    """
    Validate that the uploaded file is a PDF.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="File must be a PDF"
        )
    
    # Check magic bytes for PDF
    content_start = await file.read(4)
    await file.seek(0)  # Reset file pointer
    
    if content_start != b'%PDF':
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file"
        )
    
    return True

async def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    """
    Save an uploaded file to a destination path.
    """
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )
    finally:
        upload_file.file.close()

def cleanup_temp_file(file_path: Path) -> None:
    """
    Clean up temporary files.
    """
    try:
        if file_path.exists():
            file_path.unlink()
    except Exception as e:
        print(f"Warning: Failed to delete temp file {file_path}: {e}")