from dataclasses import dataclass
from enum import Enum
from app.schemas.game_schema import Action, VoteCard, EventCard, Positions, \
    PlayerGameInfo
from typing import List, Dict, Optional


@dataclass
class Votes:
    cannons: int = 0
    fire: int = 0
    water: int = 0
    britain: int = 0
    france: int = 0
    skull: int = 0
    wheel: int = 0


@dataclass
class Player:
    class Team(Enum):
        ENGLAND = "england"
        FRANCE = "france"
        DUTCH = "dutch"

    id: str
    team: str
    vote_cards: List[VoteCard] = None
    event_cards: List[EventCard] = None
    role: Optional[PlayerGameInfo.Role] = None
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
    players_info: Dict[str, Player]
    host: str
    players_position: Dict[str, Positions]
    chests_position: Chests
    votes: Optional[Votes] = Votes()
    turn: str = ""
    last_action: Optional[Action] = None
    last_votes: Optional[Votes] = None
    is_over: bool = False
    winner: Optional[str] = None

    def get_jr_caption(self) -> Optional[str]:
        for player, position in self.players_position.items():
            if position == Positions.JR1:
                return player
        return None

    @property
    def players(self):
        return list(self.players_position.keys())

    def next_turn(self):
        index = self.players.index(self.turn)
        index += 1
        if index == len(self.players):
            index = 0
        self.turn = self.players[index]

    def give_chest(self, player: str):
        self.players_info.get(player).chests += 1
