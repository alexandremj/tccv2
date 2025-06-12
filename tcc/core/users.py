import asyncio

from fastapi import HTTPException
from core.base import BaseService
from models.user import User

from db.connect import connect_db


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
    async def add_user(cls, user: dict) -> int:
        """Add a new user."""
        return await cls.repository.users.create_user(user)

    @classmethod
    async def delete_user(cls, id_: str):
        """Delete a user by ID."""
        return await cls.repository.users.delete_user(id_)


if __name__ == "__main__":
    user_service = UserService()
    asyncio.get_event_loop().run_until_complete(
        user_service.get_by_email("test@user.com")
    )
