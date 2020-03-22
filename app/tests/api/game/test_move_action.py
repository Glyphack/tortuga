from app.schemas.game_schema import Positions
from .base import BaseGameTestCase


class TestMoveAction(BaseGameTestCase):
    def test_player_move_from_ship(self):
        player_to_move = self.game.get_jr_caption()
        self._move_action(player_to_move, Positions.JR_B)

        assert self.game.players_position[player_to_move] == Positions.JR_B

    def test_player_move_from_boat_to_ship(self):
        player_to_move = self.game.get_jr_caption()
        self.game.players_position[player_to_move] = Positions.JR_B
        self._move_action(player_to_move, Positions.JR)
        assert self.game.players_position[
                   player_to_move] in Positions.jr_positions()

    def test_player_move_from_boat_to_tortuga(self):
        player_to_move = self.game.get_jr_caption()
        self.game.players_position[player_to_move] = Positions.JR_B
        self._move_action(player_to_move, Positions.TR)

        assert self.game.players_position[
                   player_to_move] in Positions.tr_positions()
