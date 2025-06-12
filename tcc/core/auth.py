import bcrypt
from datetime import datetime, timedelta, timezone
import os

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

JWT_SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if not JWT_SECRET_KEY:
    raise ValueError(
        "SECRET_KEY environment variable is not set. Please set it to a secure value."
    )


def _generate_salt() -> bytes:
    """Generate a salt for password hashing."""
    return bcrypt.gensalt(rounds=14)


def hash_password(password: str) -> bytes:
    """Generate a hash for the given password and salt."""
    salt = _generate_salt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    """Verify a plain password against a hashed password."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)

def decode_jwt(token: str) -> dict:
    """Decode a JWT token and return the payload."""
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def create_access_token(data: dict) -> str:
    """Create a JWT access token."""

    to_encode = data.copy()
    expiration = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expiration})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm="HS256")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    token_data = decode_jwt(token)
    return {"username": token_data["email"], "token": token}
