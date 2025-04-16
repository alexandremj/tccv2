from http import HTTPStatus

from models.post import PostModel


class DB:
    # todo: move this to an actual database implementation
    database = [
        PostModel(id="1", user="xande", content="hunter2"),
        PostModel(id="2", user="xande", content="pass"),
        PostModel(id="3", user="mah", content="senha")
    ]

    @classmethod
    async def get_posts(cls):
        return cls.database

    @classmethod
    async def save_post(cls, post: PostModel):
        cls.database += [post]
        return 201

    @classmethod
    async def delete_post(cls, id_: str):
        temp_database = [row for row in cls.database if row.id != id_]

        status = (
            HTTPStatus.NO_CONTENT
            if len(temp_database) < len(cls.database)
            else HTTPStatus.NOT_FOUND
        )

        cls.database = temp_database

        return status
