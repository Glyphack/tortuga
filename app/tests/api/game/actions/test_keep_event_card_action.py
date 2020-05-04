from app.models.game import Game
from app.tests.api.game.base import BaseGameTestCase


class TestKeepEventCardAction(BaseGameTestCase):
    def test_keep_event_card(self, game: Game):
        game.event_cards = ["letter-of-marque"]
        player = game.turn
        self._reveal_event_card_action(player, 0)
        assert player == game.turn
        self._keep_event_card_action(player)
        r = self._get_my_game(player).json()
        assert len(r["gameStatus"]["playerGameInfo"]["eventCards"]) > 0
        assert (
                "canUse" in r["gameStatus"]["playerGameInfo"]["eventCards"][
            0] and
                "eventCard" in r["gameStatus"]["playerGameInfo"]["eventCards"][
                    0]
        )
        assert player != game.turn
