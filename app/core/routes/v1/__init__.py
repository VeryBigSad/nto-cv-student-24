from fastapi import APIRouter
from . import classify_image, classify_text, get_by_id


router = APIRouter(prefix="/v1", tags=["v1"])
router.include_router(get_by_id.router)
router.include_router(classify_image.router)
router.include_router(classify_text.router)
