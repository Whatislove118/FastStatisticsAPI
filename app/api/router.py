from fastapi import APIRouter

from app.api.endpoints import router as statistics_router

router = APIRouter()

router.include_router(
    statistics_router,
    prefix="/statistics",
    tags=["statistics"],
)
