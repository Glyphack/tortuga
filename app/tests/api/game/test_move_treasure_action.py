from app.schemas.game_schema import Positions, TreasureHoldTeams
from .base import BaseGameTestCase


class TestMoveTreasureAction(BaseGameTestCase):
    def test_move_treasure_moves(self):
        self.game.turn = self.game.players[2]
        player = self.game.turn
        self.game.chests_position.jr_fr = 1
        self._move_treasure_action(player, TreasureHoldTeams.france).json()
        request = self._get_my_game(player).json()
        assert request["gameStatus"]["chestsPosition"]["jr_en"] == 1
        assert request["gameStatus"]["chestsPosition"]["jr_fr"] == 0

    def test_move_treasure_changes_turn(self):
        self.game.turn = self.game.players[2]
        player = self.game.turn
        self.game.chests_position.jr_fr = 1
        r = self._move_treasure_action(player, TreasureHoldTeams.france)
        print(r.json())
        assert self.game.turn != player

    def test_move_from_empty_hold(self):
        player = self.game.turn
        self.game.players_position[player] = Positions.JR1
        response = self._move_treasure_action(player, TreasureHoldTeams.france)
        assert response.status_code == 400

    def test_move_chest_not_cabin_boy(self):
        player = self.game.turn
        response = self._move_treasure_action(player, TreasureHoldTeams.france)
        assert response.status_code == 400
