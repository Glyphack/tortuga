from app.schemas.game_schema import Positions
from app.tests.api.game.base import BaseGameTestCase


class TestAtlantis(BaseGameTestCase):
    def test_reveal_atlantis_card(self, game):
        player = game.turn
        game.event_cards = ["atlantis"]
        self._reveal_event_card_action(player, 0)
        self.use_event_card_action(player, "atlantis")
        assert game.players_position[player] in Positions.fd_positions()

    def test_keep_atlantis_card(self, game):
        player = game.turn
        game.event_cards = ["atlantis"]
        self._reveal_event_card_action(player, 0)
        self._keep_event_card_action(player)
        assert game.turn != player
        self.use_event_card_action(player, "atlantis")
        assert game.players_position[player] in Positions.fd_positions()
