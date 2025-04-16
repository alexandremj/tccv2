from fastapi import HTTPException

from core.base import BaseService
from db.db import DB
from models.post import PostModel


class PostService(BaseService):
    """Operations on Post objects."""

    @classmethod
    async def get_by_id(cls, id_: str):
        posts = await DB().get_posts()
        matches = [post for post in posts if post.id == id_]

        if not matches:
            raise HTTPException(status_code=404, detail="Post not found")

        return matches[0]

    @classmethod
    async def add_post(cls, post: PostModel):
        return await DB().save_post(post)

    @classmethod
    async def delete_post(cls, id_: str):
        return await DB().delete_post(id_)

