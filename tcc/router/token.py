from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from core.auth import create_access_token, verify_password
from core.users import UserService

router = APIRouter()


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await UserService.get_by_email(email=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if verify_password(form_data.password, user.password.encode("utf-8")):
        return {
            "access_token": create_access_token({"email": user.email}),
            "token_type": "bearer",
        }
    raise HTTPException(status_code=401, detail="Incorrect username or password")
