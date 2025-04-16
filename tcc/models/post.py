from pydantic import BaseModel

class PostModel(BaseModel):
    # todo: user should be a reference to the creator of the post
    id: str
    user: str
    content: str

