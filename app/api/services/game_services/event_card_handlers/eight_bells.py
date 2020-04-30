import random
from typing import List, Optional, Tuple

from app.schemas.game_schema import Positions
from .event_card_handler import EventCardHandler


class EightBells(EventCardHandler):
    def reveal(self) -> None:
        players = self.affected_players
        move_to = self.affected_positions[1]
        random.shuffle(players)
        for player in self.affected_players:
            del self.game.players_position[player]
        for player in players:
            self.game.set_position(player, move_to)

    @property
    def affected_players(self) -> List:
        players = set()
        for player, position in self.game.players_position.items():
            if position in self.affected_positions[0]:
                players.add(player)
        return list(players)

    @property
    def affected_positions(self) -> Optional[Tuple[List, Positions]]:
        if self.game.get_position(self.player) in Positions.jr_positions():
            position = (Positions.jr_positions(), Positions.JR)
        elif self.game.get_position(self.player) in Positions.fd_positions():
            position = (Positions.fd_positions(), Positions.FD)
        elif self.game.get_position(self.player) in Positions.tr_positions():
            position = (Positions.tr_positions(), Positions.TR)
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
