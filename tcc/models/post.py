from pydantic import BaseModel

class PostModelWithoutId(BaseModel):
    # todo: user should be a reference to the creator of the post
    user: str
    content: str
    active: bool | None = True

class PostModel(BaseModel):
    # todo: user should be a reference to the creator of the post
    id: str
    user: str
    content: str
    active: bool | None = True

class PostUpdateModel(BaseModel):
    id: str
    content: str | None = None
    active: bool | None = None

class PostUserContent(BaseModel):
    user: str
    content: str


class PostContent(BaseModel):
    content: str