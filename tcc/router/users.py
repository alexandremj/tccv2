from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from core.auth import get_current_user
from core.users import UserService
from models.user import UserProfileInfo, UserWithoutPassword

router = APIRouter()

@router.get("/users/me", tags=["users"])
async def read_user_me(token: Annotated[str, Depends(get_current_user)]):
    user = await UserService.get_by_email(token["username"])
    return UserWithoutPassword(
        id=user.id,
        email=user.email,
        identification=user.identification,
    )


@router.post("/users/register", tags=["users"])
async def register_user(user: UserProfileInfo):
    return await UserService.add_user(user)
