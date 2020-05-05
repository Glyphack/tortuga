from typing import List

from .event_card_handler import EventCardHandler


class BlackSpot(EventCardHandler):
    def reveal(self):
        self.game.maroon_player(self.player)

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
