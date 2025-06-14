from fastapi import APIRouter, File, UploadFile

from core.check import CheckService

router = APIRouter()


@router.post("/check/file", tags=["check"])
async def check_file_exists(file: UploadFile = File(...)):
    return await CheckService.check_file_exists(file=file)
