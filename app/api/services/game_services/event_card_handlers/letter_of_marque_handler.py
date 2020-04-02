from typing import List

from app.schemas.game_schema import Positions
from .event_card_handler import EventCardHandler


class LetterOfMarque(EventCardHandler):
    def reveal(self):
        pass

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
    def can_keep(self):
        return True
