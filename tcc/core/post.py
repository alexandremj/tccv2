from fastapi import HTTPException

from core.base import BaseService
from core.blockchain import BlockchainRepository
from db.db import DB
from models.post import PostModel, PostModelWithoutId


class PostService(BaseService):
    """Operations on Post objects."""

    @classmethod
    async def get_by_id(cls, id_: str) -> PostModel:
        return BlockchainRepository.posts.get_post_by_id(id_)

    @classmethod
    async def add_post(cls, post: PostModelWithoutId) -> int:
        return BlockchainRepository.posts.create_post(post)

    @classmethod
    async def delete_post(cls, id_: str):
        return await DB().delete_post(id_)

