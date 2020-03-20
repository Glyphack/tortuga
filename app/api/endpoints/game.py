from fastapi import HTTPException
from fastapi.routing import APIRouter
from starlette.requests import Request

from app.api.services.game_service import (
    get_player_game,
    handle_call_for_an_attack_action, handle_attack_vote_action,
    remove_game, is_game_host,
    generate_game_schema_from_game
)
from app.schemas.auth import User
from app.schemas.game import (
    MyGameResponse,
    DoActionRequest,
    GameStatus, PlayerGameInfo, Chests
)

router = APIRouter()


@router.get("/game/my-game", response_model=MyGameResponse)
async def my_game(request: Request):
    if not request.user.is_authenticated:
        return HTTPException(status_code=401)
    game = get_player_game(request.user.username)
    if game is None:
        return MyGameResponse(game_status=None, has_game=False)

    return MyGameResponse(
        game_status=generate_game_schema_from_game(request.user.username),
        has_game=True
    )


@router.post("/game/action")
async def do_action(request: Request, action_request: DoActionRequest):
    # action_function_mapper = {
    #     Action.ActionType.VIEW_TWO_EVENT_CARDS:
    # }
    raise NotImplemented
