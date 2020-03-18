from dataclasses import dataclass
from enum import Enum
from app.schemas.game import Action, VoteCard, EventCard
from typing import List, Dict, Optional


@dataclass
class Votes:
    cannons: int
    fire: int
    water: int
    britain: int
    france: int
    skull: int
    wheel: int


@dataclass
class Player:
    class Role(Enum):
        CAPTAIN = "captain"
        FIRST_MATE = "first mate"
        CABIN_BOY = "cabin boy"
        GOVERNOR_OF_TORTUGA = "governor of tortuga"

    class Team(Enum):
        ENGLAND = "england"
        FRANCE = "france"
        DUTCH = "dutch"

    id: str
    team: str
    vote_cards: List[VoteCard] = None
    event_cards: List[EventCard] = None
    role: Optional[Role] = None


class Positions(Enum):
    FL1 = "fl_1"
    FL2 = "fl_2"
    FL3 = "fl_3"
    FL4 = "fl_4"
    FL5 = "fl_5"
    FL_EN = "fl_en"
    FL_FR = "fl_fr"
    JR1 = "jr_1"
    JR2 = "jr_2"
    JR3 = "jr_3"
    JR4 = "jr_4"
    JR5 = "jr_5"
    JR_EN = "jr_en"
    JR_FR = "jr_fr"
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
    SP = "sp"


@dataclass
class Game:
    id: str
    players: List[str]
    players_info: Dict[str, Player]
    turn: str
    players_position: Dict[str, str] = None
    chests_position: Dict[str, str] = None
    last_action: Optional[Action] = None
    last_votes: Optional[Votes] = None
    is_over: bool = False
    winner: Optional[str] = None
