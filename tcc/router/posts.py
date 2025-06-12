from fastapi import APIRouter, Depends, File, UploadFile
from typing_extensions import Annotated

from core.auth import get_current_user
from core.post import PostService
from models.post import PostModelWithoutId, PostUpdateModel

router = APIRouter()


@router.get("/posts", tags=["/posts"])
async def get(id_: str | None = None):
    """Search for a post by its id."""
    # todo: this needs pagination for scaling later on
    if id_ is None:
        return await PostService.get_all()
    return await PostService.get_by_id(id_=id_)


@router.post("/posts", tags=["/posts"])
async def post(
    token: Annotated[str, Depends(get_current_user)],
    file: UploadFile = File(...),
):
    post = PostModelWithoutId(user=token["username"], content=file)
    return await PostService.add_post(token["username"], post)


@router.patch("/posts", tags=["/posts"])
async def update(
    token: Annotated[str, Depends(get_current_user)],
    id_: str,
    file: UploadFile = File(...),
):
    post = PostUpdateModel(id=id_, content=file)
    return await PostService.update_post(token["username"], post)


@router.delete("/posts", tags=["/posts"])
async def delete(id_: str):
    return await PostService.delete_post(id_)
