from typing import List

from app.models.event_cards import EventCardsManager
from .event_card_handler import EventCardHandler


class FountainOfYouth(EventCardHandler):
    def reveal(self):
        self.game.get_player_info(self.player).event_cards.append(
            self.slug
        )

    @property
    def options(self) -> List:
        return []

    @property
    def options_operations(self) -> List:
        return []

    @property
    def can_keep(self):
        return False

    @property
    def can_use(self):
        return False

    @property
    def slug(self):
        return "fountain-of-youth"
