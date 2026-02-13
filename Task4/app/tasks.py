from fastapi import BackgroundTasks
import asyncio

async def send_booking_confirmation(email: str, event_title: str):
    # Simulate email sending
    await asyncio.sleep(1)
    print(f"✉️ Confirmation sent to {email} for {event_title}")

async def send_event_reminder(email: str, event_title: str):
    # Simulate reminder email
    await asyncio.sleep(1)
    print(f"⏰ Reminder sent to {email} for {event_title}")