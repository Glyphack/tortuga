from fastapi import HTTPException
from fastapi.routing import APIRouter
from starlette.requests import Request

from app.api.services.game_service import get_player_game, get_player_info_in_game
from app.schemas.auth import User
from app.schemas.game import (
    GetGameStatusResponse,
    DoActionRequest,
    GameStatus, PlayerGameInfo)

router = APIRouter()


@router.get("/game/my-game", response_model=GetGameStatusResponse)
async def my_game(request: Request):
    if not request.user.is_authenticated:
        return HTTPException(status_code=401)
    game = get_player_game(request.user.username)
    player_info = get_player_info_in_game(game, request.user.username)

    return GetGameStatusResponse(
        game_status=GameStatus(
            players_position=game.players_position,
            chests_position=game.chests_position,
            player_game_info=PlayerGameInfo(
                team=player_info.team,
                vote_cards=player_info.vote_cards,
                event_cards=player_info.event_cards,
                role=player_info.role
            ),
            last_action=game.last_action,
            is_over=game.is_over,
            turn=User(username=game.turn),
            winner=game.winner
        )
    )


@router.post("/game/action")
async def do_action(request: Request, action_request: DoActionRequest):
    pass
