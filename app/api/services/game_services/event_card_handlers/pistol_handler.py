from dataclasses import dataclass
from typing import List

from app.schemas.game_schema import Positions
from .event_card_handler import EventCardHandler


class Pistol(EventCardHandler):
    def reveal(self):
        player_to_maroon = self.options_operations[self.chosen_option]
        self.game.set_position(player_to_maroon, Positions.TR)

    @property
    def can_use(self):
        return len(self.affected_players) > 0

    @property
    def can_keep(self):
        return False

    @property
    def options(self) -> List:
        options = []
        for player in self.affected_players:
            options.append(f"maroon {player}")
        return options

    @property
    def options_operations(self):
        options = []
        for player in self.game.players:
            if player == self.player:
                continue
            if self.game.players_position[player] in self.affected_positions:
                options.append(player)
            return options

    @property
    def affected_positions(self):
        positions = [Positions.JR_B, Positions.FD_B]
        positions.extend(Positions.jr_positions())
        positions.extend(Positions.fd_positions())
        return positions

    @property
    def affected_players(self):
        players = self.game.players.copy()
        players.remove(self.player)
        for player in players:
            if self.game.players_position[
                    player] not in self.affected_positions:
                players.remove(player)
        return players
