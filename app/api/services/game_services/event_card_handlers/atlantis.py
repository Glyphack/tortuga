from typing import List, Optional

from app.schemas.game_schema import Positions
from .event_card_handler import EventCardHandler


class Atlantis(EventCardHandler):
    def reveal(self):
        self.game.set_position(self.player, self.available_move())

    @property
    def can_keep(self):
        return True

    @property
    def can_use(self):
        return (
                self.available_move() is not None and
                self.game.has_unfinished_voting()
        )

    def available_move(self) -> Optional[Positions]:
        if self.game.get_position(self.player) in Positions.jr_positions():
            return Positions.FD
        elif self.game.get_position(self.player) in Positions.fd_positions():
            return Positions.JR
        else:
            return None

    @property
    def options(self) -> List:
        return []

    @property
    def options_operations(self) -> List:
        return []
