from dataclasses import dataclass
from typing import List

from app.schemas.game_schema import Positions
from .event_card_handler import EventCardHandler


class LetterOfMarque(EventCardHandler):
    @property
    def can_use(self):
        if self.game.turn != self.player:
            return None
        positions = [Positions.JR_B, Positions.FD_B]
        positions.extend(Positions.tr_positions())
        can_use = False
        for player in self.game.players:
            if player == self.player:
                continue
            if self.game.players_position[player] in positions:
                can_use = True
        return can_use

    def reveal(self):
        option_opr = self.options_operations[self.chosen_option]
        self.game.set_position(option_opr.who, option_opr.where)

    @property
    def options(self) -> List:
        positions = [Positions.JR_B, Positions.FD_B]
        positions.extend(Positions.tr_positions())
        options = []
        for player in self.game.players:
            if self.game.players_position[player] in positions:
                options.append(f"{player} to jolly roger")
                options.append(f"{player} to flying dutchman ship")
        return options

    @property
    def options_operations(self):
        positions = [Positions.JR_B, Positions.FD_B]
        positions.extend(Positions.tr_positions())
        options = []
        for player in self.game.players:
            if self.game.players_position[player] in positions:
                options.extend(
                    [
                        Operation(player, Positions.JR),
                        Operation(player, Positions.FD)
                    ]
                )
            return options

    @property
    def can_keep(self):
        return True


@dataclass
class Operation:
    who: str
    where: str
