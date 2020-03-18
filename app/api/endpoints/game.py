from fastapi.routing import APIRouter
from starlette.requests import Request

from app.schemas.game import (
    GetGameStatusRequest,
    GetGameStatusResponse,
    DoActionRequest,
)

router = APIRouter()


@router.get("/game/my-game", response_model=GetGameStatusResponse)
async def my_game(request: Request, get_game_status: GetGameStatusRequest):
    pass


@router.post("/game/action")
async def do_action(request: Request, action_request: DoActionRequest):
    pass
