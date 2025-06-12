from fastapi import UploadFile
from pydantic import BaseModel


class PostModelWithoutId(BaseModel):
    user: str
    content: UploadFile | None = None
    active: bool | None = True


class PostModel(BaseModel):
    id: str
    user: str
    content: bytes
    active: bool | None = True
    creation_time: str | None = None
    update_time: str | None = None


class PostUpdateModel(BaseModel):
    id: str
    content: UploadFile | None = None
    active: bool | None = None


class PostUserContent(BaseModel):
    user: str
    content: str


class PostContent(BaseModel):
    content: UploadFile | None = None
