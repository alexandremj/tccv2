import asyncio
import uuid

from fastapi import HTTPException

from core.auth import hash_password
from core.base import BaseService
from db.connect import connect_db
from models.user import User, UserProfileInfo


class UserService(BaseService):
    """Operations on User objects."""

    @classmethod
    async def get_by_id(cls, id_: str) -> User:
        """Get user by ID."""
        with connect_db() as connection:
            with connection.cursor() as db:
                db.execute("SELECT * FROM users WHERE id = %s", (id_,))
                user = db.fetchone()
                if user is None:
                    raise HTTPException(
                        status_code=404, detail=f"User with ID {id_} not found."
                    )
                return User(**user)

    @classmethod
    async def get_by_email(cls, email: str) -> User:
        # todo: shouldnt this be get_by_username instead?
        """Get user by e-mail."""
        with connect_db() as connection:
            with connection.cursor() as db:
                db.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = db.fetchone()

                if user is None:
                    raise HTTPException(
                        status_code=404, detail=f"User with ID {email} not found."
                    )
                return User(**user)

    @classmethod
    async def add_user(cls, user: UserProfileInfo) -> dict[str, str]:
        """Add a new user."""
        with connect_db() as connection:
            with connection.cursor() as db:
                # Check if user already exists
                db.execute("SELECT * FROM users WHERE email = %s", (user.email,))
                existing_user = db.fetchone()
                if existing_user:
                    raise HTTPException(
                        status_code=400, detail="User with this email already exists."
                    )

                generated_id = str(uuid.uuid4())
                hashed_password = hash_password(user.password).decode("utf-8")

                # Insert new user
                db.execute(
                    "INSERT INTO users (id, email, password, identification) VALUES (%s, %s, %s, %s)",
                    (
                        generated_id,
                        user.email,
                        hashed_password,
                        user.identification,
                    ),
                )
                return {"id": generated_id}

if __name__ == "__main__":
    user_service = UserService()
    asyncio.get_event_loop().run_until_complete(
        user_service.get_by_email("test@user.com")
    )
