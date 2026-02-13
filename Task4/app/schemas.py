from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models import Role, BookingStatus

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# User
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Role = Role.ATTENDEE

class UserResponse(BaseModel):
    id: int
    email: str
    role: Role
    created_at: datetime
    class Config:
        from_attributes = True

# Event
class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    location: str
    date: datetime
    capacity: int

class EventResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    location: str
    date: datetime
    capacity: int
    organizer_id: int
    created_at: datetime
    class Config:
        from_attributes = True

# Booking
class BookingCreate(BaseModel):
    event_id: int

class BookingResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    status: BookingStatus
    created_at: datetime
    class Config:
        from_attributes = True