import hashlib
import os

from database import User, SessionLocal


def hash_password(password):
    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100000
    )

    return (
        salt.hex()
        + ":"
        + password_hash.hex()
    )


def verify_password(password, stored_hash):

    salt_hex, hash_hex = stored_hash.split(":")

    salt = bytes.fromhex(salt_hex)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100000
    )

    return password_hash.hex() == hash_hex


def register_user(username, password):

    db = SessionLocal()

    try:

        existing_user = (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

        if existing_user:
            return {
                "success": False,
                "message": "User already exists"
            }

        user = User(
            username=username,
            password_hash=hash_password(password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "success": True,
            "message": "User registered successfully",
            "user_id": user.id
        }

    finally:
        db.close()


def login_user(username, password):

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

        if not user:
            return {
                "success": False,
                "message": "User not found"
            }

        if not verify_password(
            password,
            user.password_hash
        ):
            return {
                "success": False,
                "message": "Invalid password"
            }

        return {
            "success": True,
            "user_id": user.id,
            "username": user.username
        }

    finally:
        db.close()