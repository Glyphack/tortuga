from app.models.game import Game
from app.tests.api.game.base import BaseGameTestCase


class TestSpanishArmadaEventCard(BaseGameTestCase):
    def test_reveal_spanish_armada_card(self, game: Game):
        game.event_cards = ["spanish-armada"]
        player = game.turn
        self._reveal_event_card_action(player, 1)
        game_response = self._get_my_game(player).json()
        assert game_response["gameStatus"]["winner"]["winnerTeam"] == "dutch"
        assert (
                len(game_response["gameStatus"]["winner"][
                        "playersTeams"]) == len(game.players)
        )
