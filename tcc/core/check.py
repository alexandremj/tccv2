from fastapi import HTTPException
from starlette.datastructures import UploadFile as StarletteUploadFile

from core.base import BaseService
from core.content_parser import ContentParser
from core.post import PostService


class CheckService(BaseService):
    """Check if content is valid."""

    @classmethod
    async def check_file_exists(cls, file: StarletteUploadFile) -> dict[str, str]:
        """
        Check whether the file was previously uploaded to the chain.

        Parameters
        ----------
        file : StarletteUploadFile
            The file to check.

        Returns
        -------
        dict
            A message indicating whether the file is valid or not.
        """
        digest = await ContentParser(file).parse()

        if not digest:
            raise HTTPException(
                status_code=400, detail="File is empty or not provided."
            )

        digest = digest.encode("utf-8")

        posts = await PostService.get_all()

        match = next((post for post in posts if post.content == digest), None)

        if match is None:
            return {"message": "File was not found in the blockchain."}

        return {
            "message": "File was found in the blockchain.",
            "creator": match.user,
            "post_id": match.id,
            "sha256_hash": digest.decode("utf-8"),
        }
