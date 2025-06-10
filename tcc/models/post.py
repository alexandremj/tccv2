from pydantic import BaseModel

class PostModelWithoutId(BaseModel):
    # todo: user should be a reference to the creator of the post
    user: str
    content: str
    active: bool | None = True

class PostModel(BaseModel):
    # todo: user should be a reference to the creator of the post
    id: str
