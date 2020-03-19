from dataclasses import dataclass
from enum import Enum
from app.schemas.game import Action, VoteCard, EventCard, Positions
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
    chests: int = 0


@dataclass
class Chests:
    fd_fr: int
    fd_en: int
    sg_nt: int
    jr_fr: int
    jr_en: int
    tr_fr: int
    tr_en: int


@dataclass
class Game:
    id: str
    players: List[str]
    players_info: Dict[str, Player]
    turn: str
    players_position: Dict[str, Positions]
    chests_position: Chests
    last_action: Optional[Action] = None
    last_votes: Optional[Votes] = None
    is_over: bool = False
    winner: Optional[str] = None
