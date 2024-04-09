from fastapi import APIRouter
from . import classify_image, classify_text


router = APIRouter(tags=["v1"])
router.include_router(classify_image.router)
router.include_router(classify_text.router)
