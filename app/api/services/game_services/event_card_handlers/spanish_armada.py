from typing import List

from .event_card_handler import EventCardHandler


class SpanishArmadaCard(EventCardHandler):
    def reveal(self):
        self.game.finish_game()

    @property
    def can_use(self):
        return False

    @property
    def can_keep(self):
        return False

    @property
    def options(self) -> List:
        return []
