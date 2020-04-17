from app.schemas.game_schema import Positions
from app.tests.api.game.base import BaseGameTestCase


class TestBlackSpot(BaseGameTestCase):
    def test_reveal_black_spot(self, game):
        player = game.turn
        game.event_cards = ["black-spot"]
        self._reveal_event_card_action(player, 1)
        assert game.players_position[player] in Positions.tr_positions()
