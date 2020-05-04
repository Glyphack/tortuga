from app.models.game import Game
from app.tests.api.game.base import BaseGameTestCase


class TestEightBells(BaseGameTestCase):
    def test_reveal_eight_bells(self, game: Game):
        player = game.turn
        position = game.get_position(player)
        # since it's random we test until we get the result!
        while game.get_position(player) == position:
            player = game.turn
            position = game.get_position(player)
            game.event_cards = ["eight-bells"]
            self._reveal_event_card_action(player, 0)
        assert game.get_position(player) != position
