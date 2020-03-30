import random
from dataclasses import dataclass, field
from typing import List

from app.schemas.game_schema import VoteCard


@dataclass
class Votes:
    vote_cards: List[VoteCard] = field(default_factory=list)
    participated_players: List[str] = field(default_factory=list)
    cannons: int = 0
    fire: int = 0
    water: int = 0
    britain: int = 0
    france: int = 0
    skull: int = 0
    wheel: int = 0


def generate_vote_card() -> VoteCard:
    return VoteCard(
        cannon=random.randint(0, 2),
        fire=random.randint(1, 3),
        water=random.randint(1, 3),
        britain=random.randint(1, 4),
        france=random.randint(1, 4),
        skull=random.randint(1, 4),
        wheel=random.randint(1, 4)
    )
