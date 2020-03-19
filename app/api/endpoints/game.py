from fastapi import HTTPException
from fastapi.routing import APIRouter
from starlette.requests import Request

from app.api.services.game_service import (
    get_player_game,
    get_player_info_in_game
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
    player_info = get_player_info_in_game(game, request.user.username)

    return MyGameResponse(
        game_status=GameStatus(
            players_position=game.players_position,
            chests_position=Chests(
                tr_en=game.chests_position.tr_en,
                tr_fr=game.chests_position.tr_fr,
                fd_fr=game.chests_position.fd_fr,
                fd_en=game.chests_position.fd_en,
                jr_fr=game.chests_position.jr_fr,
                jr_en=game.chests_position.jr_en,
                sg_nt=game.chests_position.sg_nt,
            ),
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
        ),
        has_game=True
    )


@router.post("/game/action")
async def do_action(request: Request, action_request: DoActionRequest):
    # action_function_mapper = {
    #     Action.ActionType.VIEW_TWO_EVENT_CARDS:
    # }
    raise NotImplemented
