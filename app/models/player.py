from dataclasses import field, dataclass
from typing import List, Dict

from app.api.services.game_services.event_card_handlers import (
    event_card_handlers
)
from app.models.event_cards import EventCard, EventCardsManager
from app.schemas.game_schema import Team, VoteCard, KeptEventCard


@dataclass
class Player:
    username: str
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

    def get_kept_event_cards(self, game):
        kept_event_cards = []
        for event_card_slug in self.event_cards:
            card_handler = event_card_handlers[
                event_card_slug](
                game=game, player=self.username
            )
            kept_event_cards.append(
                KeptEventCard(
                    event_card=EventCardsManager.get(event_card_slug),
                    can_use=card_handler.can_use
                )
            )
            return kept_event_cards
