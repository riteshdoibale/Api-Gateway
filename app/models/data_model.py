from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime, timedelta

class WorkDetailsModel(BaseModel):
    ticketName: Optional[str] = Field(None, max_length=100)
    workDescription: Optional[str] = Field(None, max_length=500)
    

class NewDailyWorkModel(BaseModel):
    companyName: str = Field(..., min_length=2, max_length=100, strict=True)
    teamName: str = Field(..., min_length=2, max_length=100, strict=True)
    sprintName: Optional[str] = Field(None, max_length=100)
    workDate: date = Field(default_factory=date.today)
    achievements: Optional[str] = Field(None, max_length=200)
    workDetails: Optional[List[WorkDetailsModel]] = Field(default_factory=lambda: [WorkDetailsModel()])
    
    @validator("workDate", pre=True, always=True)
    def validate_date(cls, value):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        if value > date.today():
            raise ValueError("Future Date is invalid.")
        return value
    

class UpdateDailyWorkModel(BaseModel):
    company: str = Field(..., min_length=2, max_length=100, strict=True)
    team: str = Field(..., min_length=2, max_length=100, strict=True)
    sprint: Optional[str] = Field(None, max_length=100)
    workDate: date = Field(default_factory=date.today)
    achievements: Optional[str] = Field(None, max_length=200)
    ticketId: Optional[str] = Field(None, max_length=100)
    workDescription: Optional[str] = Field(None, max_length=500)
    
    @validator("workDate", pre=True, always=True)
    def validate_date(cls, value):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        if value > date.today():
            raise ValueError("Future Date is invalid.")
        return value
    

class GetDailyWorkModel(BaseModel):
    startDate: Optional[date] = Field(default_factory=lambda: date.today() - timedelta(days=30))
    endDate: Optional[date] = Field(default_factory=date.today)
    pageNumber: int = Field(default=1)
    pageSize: Optional[int] = Field(default=10)
    company: Optional[str] = Field(default=None, min_length=2, max_length=100, strict=True)
    team: Optional[str] = Field(default=None, min_length=2, max_length=100, strict=True)
    sprint: Optional[str] = Field(default=None, max_length=100)
    ticketId: Optional[str] = Field(default=None, max_length=100)
    
    @validator("startDate", pre=True, always=True)
    def validate_date(cls, value):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        if value > date.today():
            raise ValueError("Future Date is invalid.")
        return value
    
    @validator("endDate", pre=True, always=True)
    def validate_date(cls, value):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        if value > date.today():
            raise ValueError("Future Date is invalid.")
        return value