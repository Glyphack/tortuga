from app.models.game import Game
from app.schemas.game_schema import Positions
from app.tests.api.game.base import BaseGameTestCase


class TestUseEventCard(BaseGameTestCase):
    def test_use_event_card_after_reveal(self, game: Game):
        event_card_slug = "letter-of-marque"
        game.event_cards = ["letter-of-marque"]
        player = game.turn
        game.players_position[player] = Positions.JR_B
        self._reveal_event_card_action(player, 0)
        self.use_event_card_action(player, event_card_slug, 0)
        assert game.players_position[player] in Positions.jr_positions()
