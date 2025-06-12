from pydantic import BaseModel


class User(BaseModel):
    id: str
    email: str
    password: str
    identification: str

class UserWithoutPassword(BaseModel):
    id: str
    email: str
    identification: str


class UserProfileInfo(BaseModel):
    email: str
    password: str
    identification: str
