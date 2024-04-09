from fastapi import APIRouter

from .v1 import router as router_v1

core_router = APIRouter()
core_router.include_router(router_v1)
