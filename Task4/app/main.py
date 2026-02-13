from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
import json

from app.database import get_db, Base, engine, redis_client
from app.models import User, Event, Booking, Role, BookingStatus
from app.schemas import *
from app.auth import verify_password, get_password_hash, create_access_token
from app.dependencies import get_current_user, require_role
from app.tasks import send_booking_confirmation, send_event_reminder

app = FastAPI(title="Event Booking API", version="1.0")

# Startup: Create tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# AUTH ENDPOINTS
@app.post("/api/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@app.post("/api/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

# USER ENDPOINTS
@app.get("/api/users/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/api/users", response_model=List[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    current_user: User = Depends(require_role(Role.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

# EVENT ENDPOINTS
@app.post("/api/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: EventCreate,
    current_user: User = Depends(require_role(Role.ORGANIZER, Role.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    event = Event(**event_data.model_dump(), organizer_id=current_user.id)
    db.add(event)
    await db.commit()
    await db.refresh(event)
    
    # Invalidate cache
    await redis_client.delete("events:list")
    return event

@app.get("/api/events", response_model=List[EventResponse])
async def list_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)
):
    # Try cache first
    cache_key = f"events:list:{skip}:{limit}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    result = await db.execute(select(Event).offset(skip).limit(limit))
    events = result.scalars().all()
    
    # Cache for 5 minutes
    events_dict = [EventResponse.from_orm(e).dict() for e in events]
    await redis_client.setex(cache_key, 300, json.dumps(events_dict, default=str))
    
    return events

@app.get("/api/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.delete("/api/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    current_user: User = Depends(require_role(Role.ORGANIZER, Role.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.organizer_id != current_user.id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    await db.delete(event)
    await db.commit()
    await redis_client.delete("events:list")

# BOOKING ENDPOINTS
@app.post("/api/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Get event
    result = await db.execute(select(Event).where(Event.id == booking_data.event_id))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check existing booking
    result = await db.execute(
        select(Booking).where(
            Booking.user_id == current_user.id,
            Booking.event_id == booking_data.event_id,
            Booking.status != BookingStatus.CANCELLED
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already booked")
    
    # Check capacity
    result = await db.execute(
        select(func.count(Booking.id)).where(
            Booking.event_id == booking_data.event_id,
            Booking.status == BookingStatus.CONFIRMED
        )
    )
    confirmed_count = result.scalar()
    
    booking_status = BookingStatus.CONFIRMED if confirmed_count < event.capacity else BookingStatus.WAITLISTED
    
    booking = Booking(
        user_id=current_user.id,
        event_id=booking_data.event_id,
        status=booking_status
    )
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    
    # Send confirmation email in background
    background_tasks.add_task(send_booking_confirmation, current_user.email, event.title)
    
    return booking

@app.get("/api/bookings", response_model=List[BookingResponse])
async def list_my_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Booking)
        .where(Booking.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@app.patch("/api/bookings/{booking_id}/cancel", response_model=BookingResponse)
async def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    booking.status = BookingStatus.CANCELLED
    await db.commit()
    await db.refresh(booking)
    return booking

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)