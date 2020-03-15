from typing import List, Dict

from pydantic.main import BaseModel

from app.schemas.auth import User


class Lobby(BaseModel):
    id: str
    size: int
    occupy: int
    players: List[User]
    host: User


class EventCard(BaseModel):
    description: str


# class VoteCard(BaseModel):
#     class AttackVote:
#         CANNON = 1
#         FIRE = 2
#         WATER = 3
#
#     class BrawlVote:
#         BRITAIN = 1
#         FRANCE = 2
#
#     class MutinyVote:
#         SKULL = 1
#         WHEEL = 2
#
#     top: AttackVote
#     middle: BrawlVote
#     bottom: MutinyVote


class ViewTwoEventCardsActionResponse(BaseModel):
    event_cards: List[EventCard]


class RevealOneEventCardActionResponse(BaseModel):
    event_card: EventCard


# class Action(BaseModel):
#     class ActionType:
#         VIEW_TWO_EVENT_CARDS = 1
#         REVEAL_ONE_EVENT_CARD = 2
#         FORCE_ANOTHER_PLAYER_TO_CHOOSE_CARD = 3
#         MOVE = 4
#
#     event_type: ActionType


class PlayerGameInfo(BaseModel):
    team: str
    # vote_cards: List[VoteCard]
    event_cards: List[EventCard]


class GameStatus(BaseModel):
    players_position: Dict[str, str]
    chests_position: Dict[str, str]
    player_game_info: PlayerGameInfo
    # event: Action
    is_over: bool
    turn: User
    winner: User


class GetLobbyListResponse(BaseModel):
    lobbies: List[Lobby]


class JoinLobbyRequest(BaseModel):
    lobby_id: str


class JoinLobbyResponse(BaseModel):
    success: bool
    lobby: Lobby


class LeaveLobbyRequest(BaseModel):
    lobby_id: str


class StartGameResponse(BaseModel):
    started: bool
    game_status: GameStatus


class CheckGameStatusResponse(BaseModel):
    started: bool
    game_status: GameStatus


