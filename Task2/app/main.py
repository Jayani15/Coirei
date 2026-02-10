from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List

from app.models import (
    CheckInRequest,
    CheckOutRequest,
    CheckInResponse,
    CheckOutResponse,
    AttendanceHistoryResponse,
    AttendanceRecordResponse,
    ErrorResponse
)
from app.services import AttendanceService


# Create FastAPI app
app = FastAPI(
    title="Attendance System API",
    description="A simple attendance system for employee check-in/check-out tracking",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Welcome to Attendance System API",
        "status": "running",
        "docs": "/docs"
    }


@app.post(
    "/check-in",
    response_model=CheckInResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Attendance"],
    responses={
        201: {"description": "Successfully checked in"},
        400: {"model": ErrorResponse, "description": "Already checked in"}
    }
)
async def check_in(request: CheckInRequest):
    """
    Check in an employee
    
    - **employee_id**: Unique employee identifier (e.g., EMP001)
    
    **Rules:**
    - Employee cannot check in if already checked in
    - Returns check-in timestamp
    """
    try:
        record = AttendanceService.check_in(request.employee_id)
        
        return CheckInResponse(
            message="Check-in successful",
            employee_id=record.employee_id,
            check_in_time=record.check_in_time
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post(
    "/check-out",
    response_model=CheckOutResponse,
    status_code=status.HTTP_200_OK,
    tags=["Attendance"],
    responses={
        200: {"description": "Successfully checked out"},
        400: {"model": ErrorResponse, "description": "Not checked in"}
    }
)
async def check_out(request: CheckOutRequest):
    """
    Check out an employee
    
    - **employee_id**: Unique employee identifier (e.g., EMP001)
    
    **Rules:**
    - Employee must be checked in before checking out
    - Returns check-in time, check-out time, and duration
    """
    try:
        record = AttendanceService.check_out(request.employee_id)
        
        duration = AttendanceService.calculate_duration(
            record.check_in_time,
            record.check_out_time
        )
        
        return CheckOutResponse(
            message="Check-out successful",
            employee_id=record.employee_id,
            check_in_time=record.check_in_time,
            check_out_time=record.check_out_time,
            duration_minutes=duration or 0.0
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get(
    "/attendance/{employee_id}",
    response_model=AttendanceHistoryResponse,
    status_code=status.HTTP_200_OK,
    tags=["Attendance"],
    responses={
        200: {"description": "Attendance history retrieved"},
        404: {"model": ErrorResponse, "description": "No records found"}
    }
)
async def get_attendance(employee_id: str):
    """
    Get attendance history for an employee
    
    - **employee_id**: Unique employee identifier (e.g., EMP001)
    
    **Returns:**
    - All attendance records for the specified employee
    - Each record includes check-in time, check-out time (if applicable), and duration
    """
    records = AttendanceService.get_attendance_history(employee_id)
    
    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No attendance records found for employee {employee_id}"
        )
    
    # Convert records to response format
    record_responses = []
    for record in records:
        duration = AttendanceService.calculate_duration(
            record.check_in_time,
            record.check_out_time
        )
        
        record_responses.append(
            AttendanceRecordResponse(
                employee_id=record.employee_id,
                check_in_time=record.check_in_time,
                check_out_time=record.check_out_time,
                is_checked_in=record.is_checked_in,
                duration_minutes=duration
            )
        )
    
    return AttendanceHistoryResponse(
        employee_id=employee_id,
        total_records=len(records),
        records=record_responses
    )


@app.get(
    "/status/{employee_id}",
    status_code=status.HTTP_200_OK,
    tags=["Attendance"],
    responses={
        200: {"description": "Current status retrieved"}
    }
)
async def get_status(employee_id: str):
    """
    Get current check-in status of an employee
    
    - **employee_id**: Unique employee identifier (e.g., EMP001)
    
    **Returns:**
    - Current status (checked in or checked out)
    - If checked in, returns the check-in time
    """
    current_record = AttendanceService.get_current_status(employee_id)
    
    if current_record:
        return {
            "employee_id": employee_id,
            "is_checked_in": True,
            "check_in_time": current_record.check_in_time,
            "message": "Employee is currently checked in"
        }
    else:
        return {
            "employee_id": employee_id,
            "is_checked_in": False,
            "check_in_time": None,
            "message": "Employee is currently checked out"
        }


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )