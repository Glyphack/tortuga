from typing import List

from app.schemas.game_schema import Positions
from .event_card_handler import EventCardHandler


class BlackSpot(EventCardHandler):
    def reveal(self):
        self.game.set_position(self.player, Positions.TR)

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
