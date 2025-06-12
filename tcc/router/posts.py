from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from core.auth import get_current_user
from core.post import PostService
from models.post import PostContent, PostUpdateModel

router = APIRouter()


# todo: shouldn't have the filterless option available unless in debug mode
@router.get("/posts", tags=["/posts"])
async def get(id_: str | None = None):
    """Search for a post by its id."""
    # todo[alexandremj]: this needs pagination for scaling later on
    if id_ is None:
        return await PostService.get_all()
    return await PostService.get_by_id(id_=id_)


@router.post("/posts", tags=["/posts"])
async def post(post: PostContent, token: Annotated[str, Depends(get_current_user)]):
    return await PostService.add_post(token["username"], post)


@router.patch("/posts", tags=["/posts"])
async def put(post: PostUpdateModel, token: Annotated[str, Depends(get_current_user)]):
    return await PostService.update_post(token["username"], post)


@router.delete("/posts", tags=["/posts"])
async def delete(id_: str):
    return await PostService.delete_post(id_)
