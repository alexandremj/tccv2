from core.base import BaseService
from core.blockchain import BlockchainRepository
from db.db import DB
from models.post import PostContent, PostModel, PostUserContent


class PostService(BaseService):
    """Operations on Post objects."""

    @classmethod
    async def get_by_id(cls, id_: str) -> PostModel:
        return BlockchainRepository.posts.get_post_by_id(id_)

    @classmethod
    async def add_post(cls, user: str, post: PostContent) -> int:
        return BlockchainRepository.posts.create_post(
            PostUserContent(user=user, content=post.content)
        )

    @classmethod
    async def delete_post(cls, id_: str):
        return await DB().delete_post(id_)
