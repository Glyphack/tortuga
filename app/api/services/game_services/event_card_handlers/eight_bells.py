import random
from typing import List, Optional, Set

from app.schemas.game_schema import Positions
from .event_card_handler import EventCardHandler


class EightBells(EventCardHandler):
    def reveal(self) -> None:
        players = self.affected_players
        random.shuffle(players)
        for player in players:
            self.game.set_position(player, )

    @property
    def affected_players(self) -> Set:
        players = set()
        for player, position in self.game.players_position:
            if position in self.affected_positions:
                players.add(player)
        return players

    @property
    def affected_positions(self) -> Optional[List]:
        if self.game.get_position(self.player) in Positions.jr_positions():
            position = Positions.jr_positions()
        elif self.game.get_position(self.player) in Positions.fd_positions():
            position = Positions.fd_positions()
        elif self.game.get_position(self.player) in Positions.tr_positions():
            position = Positions.tr_positions()
        else:
            return None
        return position

    @property
    def options(self) -> List:
        return []

    @property
    def options_operations(self) -> List:
        return []

    @property
    def can_keep(self) -> bool:
        return False

    @property
    def can_use(self) -> bool:
        return False
