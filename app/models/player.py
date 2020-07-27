from dataclasses import field, dataclass
from typing import List, Dict

from app.models.event_cards import EventCard
from app.schemas.game_schema import Team, VoteCard


@dataclass
class Player:
    id: str
    team: Team
    vote_cards: List[VoteCard] = field(default_factory=list)
    event_cards: List[str] = field(default_factory=list)
    seen_event_cards: Dict[int, EventCard] = field(default_factory=dict)
    chests: int = 0

    def add_event_card(self, slug) -> None:
        self.event_cards.append(slug)

    def remove_event_card(self, slug) -> None:
        self.event_cards.remove(slug)

    def has_event_card(self, slug) -> bool:
        return slug in self.event_cards
