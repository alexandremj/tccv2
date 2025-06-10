from fastapi import APIRouter

from core.post import PostService
from models.post import PostModel, PostModelWithoutId

router = APIRouter()

@router.get("/posts", tags=["/posts"])
async def get(id_: str):
    """Search for a post by its id."""
    return await PostService.get_by_id(id_=id_)

@router.post("/posts", tags=["/posts"])
async def post(post: PostModelWithoutId):
    return await PostService.add_post(post)

@router.patch("/posts", tags=["/posts"])
async def put(id_: str, post: PostModel):
    return await PostService.update_post(post)

@router.delete("/posts", tags=["/posts"])
async def delete(id_: str):
    return await PostService.delete_post(id_)

