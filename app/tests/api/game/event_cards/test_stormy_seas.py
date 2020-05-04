from app.schemas.game_schema import Positions
from app.tests.api.game.base import BaseGameTestCase


class TestStormySeas(BaseGameTestCase):
    def test_reveal_on_jr(self, game):
        player = game.turn
        game.event_cards = ["stormy-seas"]
        game.chests_position.jr_en = 1
        game.chests_position.jr_fr = 1
        game.chests_position.sg_nt = 2
        self._reveal_event_card_action(player, 0)
        assert game.chests_position.jr_en == 0
        assert game.chests_position.jr_fr == 0
        assert game.chests_position.sg_nt == 4

    def test_reveal_on_fd(self, game):
        player = game.turn
        game.event_cards = ["stormy-seas"]
        game.set_position(player, Positions.FD)
        game.chests_position.fd_en = 1
        game.chests_position.fd_fr = 1
        game.chests_position.sg_nt = 2
        self._reveal_event_card_action(player, 0)
        assert game.chests_position.fd_en == 0
        assert game.chests_position.fd_fr == 0
        assert game.chests_position.sg_nt == 4

    def test_reveal_on_tr(self, game):
        player = game.turn
        game.event_cards = ["stormy-seas"]
        game.set_position(player, Positions.TR)
        game.chests_position.tr_en = 2
        game.chests_position.tr_fr = 0
        self._reveal_event_card_action(player, 0)
        assert game.chests_position.tr_en == 1
        assert game.chests_position.tr_fr == 1
