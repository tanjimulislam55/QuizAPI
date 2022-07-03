from fastapi import APIRouter

from .endpoints import users, quizes

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(quizes.router, prefix="/quizes", tags=["quizes"])
