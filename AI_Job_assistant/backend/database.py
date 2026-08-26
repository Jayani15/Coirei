import os

from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime
)
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# -------------------------
# Database Tables
# -------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class UserMemory(Base):
    __tablename__ = "user_memory"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    key = Column(String(100), nullable=False)
    value = Column(Text, nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# -------------------------
# Create Tables
# -------------------------

def create_tables():
    Base.metadata.create_all(bind=engine)


# -------------------------
# Save Message
# -------------------------

def save_message(user_id, role, content):

    db = SessionLocal()

    try:
        message = Message(
            user_id=user_id,
            role=role,
            content=content
        )

        db.add(message)
        db.commit()

    finally:
        db.close()


# -------------------------
# Get Chat History
# -------------------------

def get_chat_history(user_id):

    db = SessionLocal()

    try:
        messages = (
            db.query(Message)
            .filter(Message.user_id == user_id)
            .order_by(Message.created_at)
            .all()
        )

        return [
            {
                "role": message.role,
                "content": message.content
            }
            for message in messages
        ]

    finally:
        db.close()


# -------------------------
# Save Long-Term Memory
# -------------------------
def save_memory(user_id, key, value):

    db = SessionLocal()

    try:
        existing = (
            db.query(UserMemory)
            .filter(
                UserMemory.user_id == user_id,
                UserMemory.key == key
            )
            .first()
        )

        if existing:
            existing.value = value
        else:
            memory = UserMemory(
                user_id=user_id,
                key=key,
                value=value
            )

            db.add(memory)

        db.commit()

    finally:
        db.close()


def get_user_memory(user_id):

    db = SessionLocal()

    try:
        memories = (
            db.query(UserMemory)
            .filter(UserMemory.user_id == user_id)
            .all()
        )

        return {
            memory.key: memory.value
            for memory in memories
        }

    finally:
        db.close()