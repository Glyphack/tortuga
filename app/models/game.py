from dataclasses import dataclass
from enum import Enum
from app.schemas.game import Action, VoteCard, EventCard
from typing import List, Dict, Optional


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


@dataclass
class Game:
    id: str
    players: List[str]
    players_info: Dict[str, Player]
    turn: str
    players_position: Dict[str, str] = None
    chests_position: Dict[str, str] = None
    last_action: Optional[Action] = None
    is_over: bool = False
    winner: Optional[str] = None
