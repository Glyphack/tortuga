from app.models.game import Game
from .base import BaseGameTestCase


class TestKeepEventCardAction(BaseGameTestCase):
    def test_keep_event_card(self, game: Game):
        game.event_cards = ["letter-of-marque"]
        player = game.turn
        self._reveal_event_card_action(player, 1)
        assert player == game.turn
        self._keep_event_card_action(player)
        assert len(game.players_info[player].event_cards) > 0
        assert player != game.turn
