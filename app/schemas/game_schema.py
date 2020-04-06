from enum import Enum
from typing import Dict, List, Optional, Union

from fastapi_utils.api_model import APIModel
from pydantic.main import BaseModel

from app.schemas.auth import User


class TreasureHoldTeams(str, Enum):
    britain = "BRITAIN"
    france = "FRANCE"


class Positions(str, Enum):
    FD = "fd"
    FD1 = "fd_1"
    FD2 = "fd_2"
    FD3 = "fd_3"
    FD4 = "fd_4"
    FD5 = "fd_5"
    FD_EN = "fd_en"
    FD_FR = "fd_fr"
    FD_B = "fd_b"
    JR = "jr"
    JR1 = "jr_1"
    JR2 = "jr_2"
    JR3 = "jr_3"
    JR4 = "jr_4"
    JR5 = "jr_5"
    JR_EN = "jr_en"
    JR_FR = "jr_fr"
    JR_B = "jr_b"
    TR = "tr"
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

    @classmethod
    def fd_positions(cls):
        return [cls.FD1, cls.FD2, cls.FD3, cls.FD4, cls.FD5]

    @classmethod
    def jr_positions(cls):
        return [cls.JR1, cls.JR2, cls.JR3, cls.JR4, cls.JR5]

    @classmethod
    def tr_positions(cls):
        return [
            cls.TR1, cls.TR2, cls.TR3, cls.TR4, cls.TR5,
            cls.TR6, cls.TR7, cls.TR8, cls.TR9
        ]


class VoteCard(APIModel):
    cannon: int
    fire: int
    water: int
    britain: int
    france: int
    skull: int
    wheel: int


class State(str, Enum):
    Success = "success"
    Failed = "failed"
    InProgress = "in_progress"


class EventCard(APIModel):
    slug: str
    title: str
    description: str
    image_url: str


class ViewTwoEventCardsActionData(APIModel):
    who_viewed: str


class RevealOneEventCardActionData(APIModel):
    player: str
    event_card: EventCard
    can_keep: bool
    event_card_options: List[str]


class ForceAnotherPlayerToChooseCardActionData(APIModel):
    player: str
    forced_player: str


class SeeEventCardOptionsActionData(APIModel):
    player: str
    options: List[str]
    can_use: bool


class UseEventCardActionData(APIModel):
    who: str
    event_card: str
    message: str


class CaptainCallForAttackData(APIModel):
    which_captain: User
    state: State
    from_other_ship: bool
    participating_players: List[str] = []
    vote_results: List[VoteCard] = []


class MaroonAnyCrewMateToTortugaActionData(APIModel):
    marooned_crew: str


class CallForMutinyActionData(APIModel):
    captain: str
    state: State
    participating_players: List[str] = []
    vote_results: List[VoteCard] = []


class MoveTreasureActionData(APIModel):
    cabin_boy: str
    from_hold: TreasureHoldTeams
    to_hold: TreasureHoldTeams


class CallForBrawlActionData(APIModel):
    governor: str
    state: State
    participating_players: List[str]
    vote_results: List[VoteCard] = []


class PutChestActionData(APIModel):
    where: Positions


class Action(APIModel):
    class ActionType(Enum):
        VIEW_TWO_EVENT_CARDS = "view two event cards"
        REVEAL_EVENT_CARD = "reveal one event card"
        FORCE_ANOTHER_PLAYER_TO_CHOOSE_CARD = (
            "force another player to choose card"
        )
        KEEP_EVENT_CARD = "KEEP-EVENT-CARD"
        SEE_EVENT_CARD_OPTIONS = "SEE-EVENT-CARD-OPTIONS"
        USE_EVENT_CARD = "USE-EVENT-CARD"
        MOVE = "move"
        CALL_FOR_AN_ATTACK = "call for an attack"
        MAROON_ANY_CREW_MATE_TO_TORTUGA = "maroon any crew mate to tortuga"
        CALL_FOR_A_MUTINY = "call for a mutiny"
        MOVE_TREASURE = "move treasure"
        CALL_FOR_BRAWL = "call for brawl"
        VOTE = "vote"
        PUT_CHEST = "put chest"

    action_type: ActionType
    action_data: Union[
        ViewTwoEventCardsActionData,
        RevealOneEventCardActionData,
        ForceAnotherPlayerToChooseCardActionData,
        SeeEventCardOptionsActionData,
        CaptainCallForAttackData,
        MaroonAnyCrewMateToTortugaActionData,
        CallForMutinyActionData,
        MoveTreasureActionData,
        CallForBrawlActionData,
        PutChestActionData
    ] = None


class PlayerGameInfo(APIModel):
    class Role(Enum):
        CAPTAIN = "captain"
        FIRST_MATE = "first mate"
        CABIN_BOY = "cabin boy"
        GOVERNOR_OF_TORTUGA = "governor of tortuga"

    team: str
    vote_cards: Optional[List[VoteCard]] = None
    event_cards: Optional[List[EventCard]] = None
    seen_event_cards: Optional[List[EventCard]] = None
    role: Optional[Role]
    available_actions: List[Action.ActionType]
    chests: int = 0


class Chests(BaseModel):
    fd_fr: int
    fd_en: int
    sg_nt: int
    jr_fr: int
    jr_en: int
    tr_fr: int
    tr_en: int


class GameStatus(APIModel):
    players_position: Dict[str, Positions]
    chests_position: Chests
    player_game_info: PlayerGameInfo
    event_cards_deck_count: int
    last_action: Optional[Action] = None
    is_over: bool = False
    turn: User
    winner: Optional[str] = None


class MyGameResponse(APIModel):
    game_id: str
    game_status: Optional[GameStatus]
    has_game: bool


class ViewTwoEventCardsPayload(APIModel):
    event_cards_indexes: List[int]


class MovePayload(APIModel):
    move_where: Positions


class MaroonCrewMateToTortugaPayload(APIModel):
    crew_to_maroon: str


class MoveTreasurePayload(APIModel):
    from_hold: TreasureHoldTeams


class VotePayload(APIModel):
    vote_card_index: int


class PutChestPayload(APIModel):
    class Team(str, Enum):
        britain = "BRITAIN"
        france = "FRANCE"

    which_team: Team
    from_which_team: Optional[Team]


class RevealEventCardPayload(APIModel):
    event_card_index: int


class SeeEventCardOptionsPayload(APIModel):
    event_card_to_see_slug: str


class UseEventCardPayload(APIModel):
    event_card_to_use: str
    event_card_option_index: Optional[int]


PayloadType = Optional[
    Union[
        ViewTwoEventCardsPayload,
        MovePayload,
        MaroonCrewMateToTortugaPayload,
        MoveTreasurePayload,
        VotePayload,
        PutChestPayload,
        RevealEventCardPayload,
        SeeEventCardOptionsPayload,
        UseEventCardPayload,
    ]
]


class DoActionRequest(APIModel):
    game_id: str
    action: Action
    payload: PayloadType = None
