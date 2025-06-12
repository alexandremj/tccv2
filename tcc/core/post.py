from fastapi import HTTPException
from web3.exceptions import ContractLogicError

from core.base import BaseService
from core.blockchain import BlockchainRepository
from core.content_parser import ContentParser
from core.users import UserService
from models.post import (
    PostContent,
    PostModel,
    PostUpdateModel,
    PostUserContent,
)


class PostService(BaseService):
    """Operations on Post objects."""

    @classmethod
    async def get_by_id(cls, id_: str) -> PostModel:
        try:
            return BlockchainRepository.instance().posts.get_post_by_id(id_)
        except ContractLogicError as e:
            raise HTTPException(
                status_code=404, detail=f"Post with ID {id_} not found."
            ) from e

    @classmethod
    async def get_all(cls) -> list[PostModel]:
        return BlockchainRepository.instance().posts.get_all_posts()

    @classmethod
    async def add_post(cls, user: str, post: PostContent) -> int:
        user = await UserService().get_by_email(user)
        parsed_content = await ContentParser(post.content).parse()
        return BlockchainRepository.instance().posts.create_post(
            PostUserContent(user=user.id, content=parsed_content)
        )

    @classmethod
    async def update_post(cls, user_email: str, post: PostUpdateModel) -> PostModel:
        commited_post = await cls.get_by_id(post.id)
        user = await UserService().get_by_email(user_email)

        if commited_post.user != user.id:
            raise HTTPException(
                status_code=403, detail="You are not allowed to update this post."
            )

        if post.content is not None:
            parsed_content = await ContentParser(post.content).parse()
            return (
                BlockchainRepository()
                .instance()
                .posts.update_post_content(post.id, parsed_content)
            )
        return BlockchainRepository().instance().posts.get_post_by_id(post.id)
