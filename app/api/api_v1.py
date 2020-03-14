from fastapi import APIRouter

from app.api.endpoints import auth
from app.api.endpoints import lobby

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(lobby.router, tags=["lobby"])
