from dataclasses import field, dataclass
from typing import List

from app.models.event_cards import EventCard
from app.schemas.game_schema import Team, VoteCard, KeptEventCard


@dataclass
class Player:
    id: str
    team: Team
    vote_cards: List[VoteCard] = field(default_factory=list)
    event_cards: List[EventCard] = field(default_factory=list)
    seen_event_cards: List[EventCard] = field(default_factory=list)
    chests: int = 0

    def get_kept_event_cards(self):
        kept_event_cards = []
        for event_card in self.event_cards:
            kept_event_cards.append(
                KeptEventCard(
                    event_card=event_card,
                    can_use=True
                )
            )
        return kept_event_cards
