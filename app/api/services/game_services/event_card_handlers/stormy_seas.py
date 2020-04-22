from typing import List

from app.schemas.game_schema import Positions
from .event_card_handler import EventCardHandler


class StormySeas(EventCardHandler):
    def reveal(self) -> None:
        if self.game.get_position(self.player) in Positions.jr_positions():
            treasures = (
                    self.game.chests_position.jr_en +
                    self.game.chests_position.jr_fr
            )
            self.game.chests_position.jr_en = 0
            self.game.chests_position.jr_fr = 0
        elif self.game.get_position(self.player) in Positions.fd_positions():
            treasures = (
                    self.game.chests_position.fd_en +
                    self.game.chests_position.fd_fr
            )
            self.game.chests_position.fd_fr = 0
            self.game.chests_position.fd_en = 0
        elif self.game.get_position(self.player) in Positions.tr_positions():
            self.game.chests_position.tr_fr = 1
            self.game.chests_position.tr_en = 1
            return
        else:
            return
        self.game.chests_position.sg_nt += treasures

    @property
    def options(self) -> List:
        return []

    @property
    def options_operations(self) -> List:
        return []

    @property
    def can_keep(self) -> bool:
        return False

    def can_use(self) -> bool:
        return False
