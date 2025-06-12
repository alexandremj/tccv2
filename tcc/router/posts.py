from fastapi import APIRouter

from core.auth import get_current_user
from core.post import PostService
from models.post import PostContent, PostModel

from typing_extensions import Annotated
from fastapi import Depends

router = APIRouter()

@router.get("/posts", tags=["/posts"])
async def get(id_: str):
    """Search for a post by its id."""
    return await PostService.get_by_id(id_=id_)

@router.post("/posts", tags=["/posts"])
async def post(post: PostContent, token: Annotated[str, Depends(get_current_user)]):
    return await PostService.add_post(token["username"], post)

@router.patch("/posts", tags=["/posts"])
async def put(id_: str, post: PostModel):
    return await PostService.update_post(post)

@router.delete("/posts", tags=["/posts"])
async def delete(id_: str):
    return await PostService.delete_post(id_)

