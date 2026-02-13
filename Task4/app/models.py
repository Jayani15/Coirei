from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class Role(str, enum.Enum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    ATTENDEE = "attendee"

class BookingStatus(str, enum.Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    WAITLISTED = "waitlisted"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.ATTENDEE)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    organized_events = relationship("Event", back_populates="organizer")
    bookings = relationship("Booking", back_populates="user")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    location = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    organizer = relationship("User", back_populates="organized_events")
    bookings = relationship("Booking", back_populates="event")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    status = Column(Enum(BookingStatus), default=BookingStatus.CONFIRMED)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="bookings")
    event = relationship("Event", back_populates="bookings")