from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
import pytz

class AddAuditModel(BaseModel):
    previousData: str = Field(..., min_length=1, strict=True, description="Encrypted string of previous data")
    modifiedData: str = Field(..., min_length=1, strict=True, description="Encrypted string of modified data")
    modifiedDate: str = Field(..., description="Full datetime in Indian timezone")

    @validator("modifiedDate", pre=True, always=True)
    def validate_modified_date(cls, value):
        try:
            dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            india = pytz.timezone("Asia/Kolkata")
            dt = india.localize(dt)
            return dt.strftime("%Y-%m-%d %H:%M:%S %Z")
        except Exception:
            raise ValueError("modifiedDate must be in format 'YYYY-MM-DD HH:MM:SS'")