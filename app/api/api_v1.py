from fastapi import APIRouter

from app.api.endpoints import auth
from app.api.endpoints import lobby
from app.api.endpoints import game

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(lobby.router, tags=["lobby"])
api_router.include_router(game.router, tags=["game"])
