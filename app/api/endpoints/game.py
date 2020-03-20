from fastapi import HTTPException
from fastapi.routing import APIRouter
from starlette.requests import Request

from app.api.services.game_services.service import (
    get_player_game,
    remove_game, is_game_host,
    generate_game_schema_from_game,
    get_action_handler)
from app.schemas.game_schema import (
    MyGameResponse,
    DoActionRequest,
)

router = APIRouter()


@router.get("/game/my-game", response_model=MyGameResponse)
async def my_game(request: Request):
    if not request.user.is_authenticated:
        return HTTPException(status_code=401)
    game = get_player_game(request.user.username)
    if game is None:
        return MyGameResponse(game_id="", game_status=None, has_game=False)

    return MyGameResponse(
        game_id=game.id,
        game_status=generate_game_schema_from_game(request.user.username),
        has_game=True
    )


@router.post("/game/action")
async def do_action(request: Request, action_request: DoActionRequest):
    if not request.user.is_authenticated:
        return HTTPException(status_code=401)
    game = get_player_game(request.user.username)
    if game is None:
        return MyGameResponse(game_status=None, has_game=False)

    get_action_handler(
        game,
        request.user.username,
        action_request.action,
        payload=action_request.payload
    ).execute()

    return


@router.post("/game/stop")
async def stop_game(request: Request, game_id: str):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=401)
    username = request.user.username
    if is_game_host(get_player_game(username), username):
        remove_game(game_id)
