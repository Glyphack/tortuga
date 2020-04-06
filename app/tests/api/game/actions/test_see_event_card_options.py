from app.models.game import Game
from app.schemas.game_schema import Positions
from app.tests.api.game.base import BaseGameTestCase


class TestSeeEventCardOptions(BaseGameTestCase):
    def test_see_event_card_option(self, game: Game):
        event_card_slug = "letter-of-marque"
        game.event_cards = [event_card_slug]
        player = game.turn
        game.next_turn()
        game.players_position[player] = Positions.TR1
        self.see_event_card_options(game.turn, event_card_slug)
        response = self._get_my_game(game.turn).json()

        action_data = response["gameStatus"]["lastAction"]["actionData"]
        assert len(action_data["options"]) == 2
        assert action_data["canUse"] is True
