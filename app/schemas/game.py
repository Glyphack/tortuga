from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic.main import BaseModel

from app.schemas.auth import User


class Positions(Enum):
    FD1 = "fd_1"
    FD2 = "fd_2"
    FD3 = "fd_3"
    FD4 = "fd_4"
    FD5 = "fd_5"
    FD_EN = "fd_en"
    FD_FR = "fd_fr"
    FD_B = "fd_b"
    JR1 = "jr_1"
    JR2 = "jr_2"
    JR3 = "jr_3"
    JR4 = "jr_4"
    JR5 = "jr_5"
    JR_EN = "jr_en"
    JR_FR = "jr_fr"
    JR_B = "jr_b"
    TR1 = "tr_1"
    TR2 = "tr_2"
    TR3 = "tr_3"
    TR4 = "tr_4"
    TR5 = "tr_5"
    TR6 = "tr_6"
    TR7 = "tr_7"
    TR8 = "tr_8"
    TR9 = "tr_9"
    TR_EN = "tr_en"
    TR_FR = "tr_fr"
    SP = "sg_nt"


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


class GovernorOfTortugaCallForBrawlData(BaseModel):
    governor: str


class PutChestData(BaseModel):
    where: Positions


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
        PUT_CHEST = "put chest"

    action_type: ActionType
    action_data: Union[
        ViewTwoEventCardsActionData,
        RevealOneEventCardActionData,
        ForceAnotherPlayerToChooseCardActionData,
        CaptainCallForAttackActionData,
        MaroonAnyCrewMateToTortuga,
        FirstMateCallForAMutiny,
        CabinBoysMoveTreasureData,
        GovernorOfTortugaCallForBrawlData,
        PutChestData
    ] = None


class PlayerGameInfo(BaseModel):
    class Role(Enum):
        CAPTAIN = "captain"
        FIRST_MATE = "first mate"
        CABIN_BOY = "cabin boy"
        GOVERNOR_OF_TORTUGA = "governor of tortuga"

    team: str
    vote_cards: Optional[List[VoteCard]] = None
    event_cards: Optional[List[EventCard]] = None
    role: Optional[Role]


class Chests(BaseModel):
    fd_fr: int
    fd_en: int
    sg: int
    jr_fr: int
    jr_en: int
    tr_fr: int
    tr_en: int


class GameStatus(BaseModel):
    players_position: Dict[str, Positions]
    chests_position: Chests
    player_game_info: PlayerGameInfo
    last_action: Optional[Action] = None
    is_over: bool = False
    turn: User
    winner: Optional[User] = None


class MyGameResponse(BaseModel):
    game_status: Optional[GameStatus]
    has_game: bool


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
    payload: Union[
        ViewTwoEventCardsPayload,
        MovePayload,
        MaroonCrewMateToTortugaPayload,
        CabinBoyMoveTreasurePayload,
        VotePayload
    ]
