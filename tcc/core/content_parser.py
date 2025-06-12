import hashlib

from fastapi import HTTPException
from starlette.datastructures import UploadFile as StarletteUploadFile


class ContentParser:
    def __init__(self, content):
        self.content = content

    async def parse(self) -> str:
        _content = self.content

        if isinstance(_content, StarletteUploadFile):
            content: bytes = await _content.read()
            if not content:
                raise HTTPException(
                    status_code=400, detail="File is empty or not provided."
                )
        elif isinstance(_content, str):
            content: bytes = _content.encode("utf-8")
            if not content:
                raise HTTPException(
                    status_code=400, detail="Content is empty or not provided."
                )
        else:
            raise HTTPException(
                status_code=400, detail="Content must be a string or an UploadFile."
            )

        return hashlib.sha256(content).hexdigest()
