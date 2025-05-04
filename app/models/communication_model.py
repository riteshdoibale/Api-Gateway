from typing import Optional
from pydantic import BaseModel, Field


class SendOtpModel(BaseModel):
    transactionId: Optional[str] = Field(default=None, max_length=100, strict=True)


class ResendOtpModel(BaseModel):
    transactionId: str = Field(..., max_length=100)
   

class ValidateOtpModel(BaseModel):
    transactionId: str = Field(..., max_length=100)
    otp: str = Field(..., min_length=6, max_length=6)
