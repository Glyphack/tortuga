from app.models.game import Game
from app.tests.api.game.base import BaseGameTestCase


class TestFountainOfYouth(BaseGameTestCase):
    def test_reveal_fountain_of_youth_dodge_maroon(self, game: Game):
        player = game.turn
        game.event_cards = ["fountain-of-youth"]
        self._reveal_event_card_action(player, 0)
        self._keep_event_card_action(player)
        response = self._get_my_game(player).json()
        assert (
            response["gameStatus"]["playerGameInfo"]["eventCards"][0][
                "eventCard"]["slug"] == "fountain-of-youth"
        )
        player_position = game.get_position(player)
        game.maroon_player(player)
        assert game.get_position(player) == player_position
