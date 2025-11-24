from fastapi import APIRouter

from .admin import router as admin_router
from .recipes import router as recipes_router
from .users import router as users_router

api_router = APIRouter()

api_router.include_router(recipes_router, prefix="/recipes", tags=["recipes"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
