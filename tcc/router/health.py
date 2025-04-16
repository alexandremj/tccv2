from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["health"])
async def root():
    return {"message": "health-ok"}
