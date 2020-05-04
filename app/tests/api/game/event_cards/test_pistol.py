from app.models.game import Game
from app.schemas.game_schema import Positions
from app.tests.api.game.base import BaseGameTestCase


class TestPistolEventCard(BaseGameTestCase):
    def test_reveal_pistol_card(self, game: Game):
        game.event_cards = ["pistol"]
        player = game.turn
        self._reveal_event_card_action(player, 0)
        game_response = self._get_my_game(player).json()
        assert (
                game_response["gameStatus"]["lastAction"][
                    "actionType"] == "reveal one event card"
        )
        assert len(game_response["gameStatus"]["lastAction"][
                       "actionData"]["eventCardOptions"]) == 3
        self.use_event_card_action(player, "pistol", 0)
        assert list(game.players_position.values())[
                   1] in Positions.tr_positions()
