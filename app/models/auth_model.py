from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class SignUpModel(BaseModel):
    premiumMember : Optional[bool] = False
    fullName : str = Field(..., min_length=2, max_length=100, strict=True)
    mobileNumber : str = Field(..., min_length=10, max_length=10, strict=True)
    userName : EmailStr = Field(..., min_length=2, max_length=50,strict=True)
    password : str = Field(..., min_length=10, max_length=200, strict=True)
    
class SignInModel(BaseModel):
    userName : EmailStr = Field(..., min_length=2, max_length=50, strict=True)
    password : str = Field(..., min_length=10, max_length=200, strict=True)