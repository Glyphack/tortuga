from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic.main import BaseModel

from app.schemas.auth import User


class VoteCard(BaseModel):
    class AttackVote(Enum):
        CANNON = "cannon"
        FIRE = "fire"
        WATER = "water"

    class BrawlVote(Enum):
        BRITAIN = "britain"
        FRANCE = "france"

    class MutinyVote(Enum):
        SKULL = "skull"
        WHEEL = "wheel"

    top: AttackVote
    middle: BrawlVote
    bottom: MutinyVote


class EventCard(BaseModel):
    description: str


class ViewTwoEventCardsActionData(BaseModel):
    who: User


class RevealOneEventCardActionData(BaseModel):
    who: User


class ForceAnotherPlayerToChooseCardActionData(BaseModel):
    player: User
    forced_player: User


class CaptainCallForAttackActionData(BaseModel):
    captain: User


class MaroonAnyCrewMateToTortuga(BaseModel):
    captain: User
    crew: User


class FirstMateCallForAMutiny(BaseModel):
    first_mate: User


class CabinBoysMoveTreasureData(BaseModel):
    cabin_boy: User
    from_where: str
    to_where: str


class GovernorOfTortugaCallForBrawl(BaseModel):
    governor: str


class Action(BaseModel):
    class ActionType(Enum):
        VIEW_TWO_EVENT_CARDS = "view two event cards"
        REVEAL_ONE_EVENT_CARD = "reveal one event card"
        FORCE_ANOTHER_PLAYER_TO_CHOOSE_CARD = (
            "force another player to choose card"
        )
        MOVE = "move"
        CAPTAIN_CALL_FOR_AN_ATTACK = "call for an attack"
        MAROON_ANY_CREW_MATE_TO_TORTUGA = "maroon any crew mate to tortuga"
        FIRST_MATE_CALL_FOR_A_MUTINY = "first mate call for a mutiny"
        CABIN_BOYS_MOVE_TREASURE = "cabin boys move treasure"
        GOVERNOR_OF_TORTUGA_CALL_FOR_BRAWL = "call for brawl"
        VOTE = "vote"

    action_type: ActionType
    action_data: Union[
        ViewTwoEventCardsActionData,
        RevealOneEventCardActionData,
        ForceAnotherPlayerToChooseCardActionData,
        CaptainCallForAttackActionData,
        MaroonAnyCrewMateToTortuga,
        FirstMateCallForAMutiny,
        CabinBoysMoveTreasureData,
        GovernorOfTortugaCallForBrawl
    ]


class PlayerGameInfo(BaseModel):
    class Role(Enum):
        CAPTAIN = "captain"
        FIRST_MATE = "first mate"
        CABIN_BOY = "cabin boy"
        GOVERNOR_OF_TORTUGA = "governor of tortuga"

    team: str
    vote_cards: List[VoteCard]
    event_cards: List[EventCard]
    role: Role


class GameStatus(BaseModel):
    players_position: Dict[str, str]
    chests_position: Dict[str, str]
    player_game_info: PlayerGameInfo
    last_action: Optional[Action]
    is_over: bool
    turn: User
    winner: User


class GetGameStatusRequest(BaseModel):
    game_id: str


class GetGameStatusResponse(BaseModel):
    game_status: GameStatus


class ViewTwoEventCardsPayload(BaseModel):
    choices: List[int]


class MovePayload(BaseModel):
    where: str


class MaroonCrewMateToTortugaPayload(BaseModel):
    who: User


class CabinBoyMoveTreasurePayload(BaseModel):
    where: str
    to_where: str


class VotePayload(BaseModel):
    vote_card: VoteCard


class DoActionRequest(BaseModel):
    game_id: str
    action: Action
    payload: Optional[
        ViewTwoEventCardsPayload,
        MovePayload,
        MaroonCrewMateToTortugaPayload,
        CabinBoyMoveTreasurePayload,
        VotePayload
    ]
