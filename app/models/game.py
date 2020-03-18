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
    last_action: Action = None
    is_over: bool = False
    turn: int = 0
    winner: str = None
