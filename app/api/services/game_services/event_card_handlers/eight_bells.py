import random
from typing import List, Optional, Tuple

from app.schemas.game_schema import Positions
from .event_card_handler import EventCardHandler


class EightBells(EventCardHandler):
    def reveal(self) -> None:
        players = self.affected_players
        move_to_positions = []

        for player in players:
            move_to_positions.append(self.game.players_position.pop(player))
        random.shuffle(players)
        for player, position in zip(
                players,
                move_to_positions
        ):
            self.game.players_position[player] = position

    @property
    def affected_players(self) -> List:
        players = set()
        for player, position in self.game.players_position.items():
            if position in self.affected_positions:
                players.add(player)
        return list(players)

    @property
    def affected_positions(self) -> Optional[List[Positions]]:
        if self.game.get_position(self.player) in Positions.jr_positions():
            positions = Positions.jr_positions()
        elif self.game.get_position(self.player) in Positions.fd_positions():
            positions = Positions.fd_positions()
        elif self.game.get_position(self.player) in Positions.tr_positions():
            positions = Positions.tr_positions()
        else:
            return None
        return positions

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
