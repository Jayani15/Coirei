from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class CheckInRequest(BaseModel):
    """Request model for check-in"""
    employee_id: str = Field(..., min_length=1, description="Employee ID (e.g., EMP001)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "EMP001"
            }
        }


class CheckOutRequest(BaseModel):
    """Request model for check-out"""
    employee_id: str = Field(..., min_length=1, description="Employee ID (e.g., EMP001)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "EMP001"
            }
        }


class CheckInResponse(BaseModel):
    """Response model for successful check-in"""
    message: str
    employee_id: str
    check_in_time: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Check-in successful",
                "employee_id": "EMP001",
                "check_in_time": "2024-02-08T09:00:00"
            }
        }


class CheckOutResponse(BaseModel):
    """Response model for successful check-out"""
    message: str
    employee_id: str
    check_in_time: datetime
    check_out_time: datetime
    duration_minutes: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Check-out successful",
                "employee_id": "EMP001",
                "check_in_time": "2024-02-08T09:00:00",
                "check_out_time": "2024-02-08T17:00:00",
                "duration_minutes": 480.0
            }
        }


class AttendanceRecordResponse(BaseModel):
    """Response model for a single attendance record"""
    employee_id: str
    check_in_time: datetime
    check_out_time: Optional[datetime]
    is_checked_in: bool
    duration_minutes: Optional[float] = None


class AttendanceHistoryResponse(BaseModel):
    """Response model for attendance history"""
    employee_id: str
    total_records: int
    records: List[AttendanceRecordResponse]
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "EMP001",
                "total_records": 2,
                "records": [
                    {
                        "employee_id": "EMP001",
                        "check_in_time": "2024-02-08T09:00:00",
                        "check_out_time": "2024-02-08T17:00:00",
                        "is_checked_in": False,
                        "duration_minutes": 480.0
                    }
                ]
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Bad Request",
                "detail": "Employee is already checked in"
            }
        }