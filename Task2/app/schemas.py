from datetime import datetime
from typing import Optional


class AttendanceRecord:
    """Internal data structure for storing attendance records"""
    
    def __init__(self, employee_id: str, check_in_time: datetime):
        self.employee_id = employee_id
        self.check_in_time = check_in_time
        self.check_out_time: Optional[datetime] = None
        self.is_checked_in = True
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "employee_id": self.employee_id,
            "check_in_time": self.check_in_time.isoformat(),
            "check_out_time": self.check_out_time.isoformat() if self.check_out_time else None,
            "is_checked_in": self.is_checked_in
        }