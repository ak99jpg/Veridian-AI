from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class InvoiceData(BaseModel):
    """
    Invoice data model for extracted information
    """
    vendor_name: Optional[str] = Field(None, description="Name of the vendor/supplier")
    invoice_date: Optional[date] = Field(None, description="Date of the invoice")
    total_amount: Optional[float] = Field(None, description="Total amount of the invoice")
    energy_consumption_kwh: Optional[float] = Field(None, description="Energy consumption in kilowatt-hours")
    
    class Config:
        json_schema_extra = {
            "example": {
                "vendor_name": "Green Energy Corp",
                "invoice_date": "2024-01-15",
                "total_amount": 1250.50,
                "energy_consumption_kwh": 8750.25
            }
        }