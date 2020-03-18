from fastapi import HTTPException
from fastapi.routing import APIRouter
from starlette.requests import Request

from app.api.services.game_service import get_player_game
from app.schemas.game import (
    GetGameStatusResponse,
    DoActionRequest,
)

router = APIRouter()


@router.get("/game/my-game", response_model=GetGameStatusResponse)
async def my_game(request: Request):
    if not request.user.is_authenticated:
        return HTTPException(status_code=401)
    game_status = get_player_game(request.user.username)
    return GetGameStatusResponse(game_status=game_status)


@router.post("/game/action")
async def do_action(request: Request, action_request: DoActionRequest):
    pass
