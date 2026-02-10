from datetime import datetime
from typing import List, Optional
from app.schemas import AttendanceRecord


# In-memory storage
attendance_records: List[AttendanceRecord] = []


class AttendanceService:
    """Service class for attendance business logic"""
    
    @staticmethod
    def check_in(employee_id: str) -> AttendanceRecord:
        """
        Check in an employee
        
        Rules:
        - Employee cannot check in if already checked in
        
        Args:
            employee_id: The employee's ID
            
        Returns:
            AttendanceRecord: The created attendance record
            
        Raises:
            ValueError: If employee is already checked in
        """
        # Check if employee is already checked in
        for record in attendance_records:
            if record.employee_id == employee_id and record.is_checked_in:
                raise ValueError(f"Employee {employee_id} is already checked in")
        
        # Create new check-in record
        new_record = AttendanceRecord(
            employee_id=employee_id,
            check_in_time=datetime.now()
        )
        
        attendance_records.append(new_record)
        return new_record
    
    @staticmethod
    def check_out(employee_id: str) -> AttendanceRecord:
        """
        Check out an employee
        
        Rules:
        - Employee must be checked in before checking out
        
        Args:
            employee_id: The employee's ID
            
        Returns:
            AttendanceRecord: The updated attendance record
            
        Raises:
            ValueError: If employee is not checked in
        """
        # Find the active check-in record
        for record in attendance_records:
            if record.employee_id == employee_id and record.is_checked_in:
                # Update the record
                record.check_out_time = datetime.now()
                record.is_checked_in = False
                return record
        
        # No active check-in found
        raise ValueError(f"Employee {employee_id} is not checked in")
    
    @staticmethod
    def get_attendance_history(employee_id: str) -> List[AttendanceRecord]:
        """
        Get attendance history for an employee
        
        Args:
            employee_id: The employee's ID
            
        Returns:
            List[AttendanceRecord]: List of all attendance records for the employee
        """
        return [
            record for record in attendance_records 
            if record.employee_id == employee_id
        ]
    
    @staticmethod
    def get_current_status(employee_id: str) -> Optional[AttendanceRecord]:
        """
        Get current check-in status of an employee
        
        Args:
            employee_id: The employee's ID
            
        Returns:
            Optional[AttendanceRecord]: Current active record if checked in, None otherwise
        """
        for record in attendance_records:
            if record.employee_id == employee_id and record.is_checked_in:
                return record
        return None
    
    @staticmethod
    def calculate_duration(check_in_time: datetime, check_out_time: Optional[datetime]) -> Optional[float]:
        """
        Calculate duration between check-in and check-out in minutes
        
        Args:
            check_in_time: Check-in timestamp
            check_out_time: Check-out timestamp
            
        Returns:
            Optional[float]: Duration in minutes, or None if not checked out
        """
        if check_out_time is None:
            return None
        
        duration = check_out_time - check_in_time
        return duration.total_seconds() / 60