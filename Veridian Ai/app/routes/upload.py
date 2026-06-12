from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
from app.services.extraction_service import ExtractionService
from app.models.invoice import InvoiceData

router = APIRouter(prefix="/upload", tags=["upload"])
logger = logging.getLogger(__name__)
extraction_service = ExtractionService()

@router.post("/invoice", response_model=InvoiceData)
async def upload_invoice(
    file: UploadFile = File(..., description="PDF invoice file")
) -> Dict[str, Any]:
    """
    Upload a PDF invoice and extract key information including:
    - vendor_name
    - invoice_date
    - total_amount
    - energy_consumption_kwh
    
    Returns extracted data as JSON
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only PDF files are accepted."
        )
    
    try:
        # Read file contents
        contents = await file.read()
        
        # Extract data using service
        extracted_data = await extraction_service.extract_from_pdf(contents, file.filename)
        
        # Log successful extraction
        logger.info(f"Successfully extracted data from {file.filename}")
        
        return JSONResponse(
            status_code=200,
            content=extracted_data
        )
    
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing invoice: {str(e)}"
        )