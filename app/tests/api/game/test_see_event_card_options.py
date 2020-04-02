from app.models.game import Game
from app.schemas.game_schema import Positions
from .base import BaseGameTestCase


class TestSeeEventCardOptions(BaseGameTestCase):
    def test_see_event_card_option(self, game: Game):
        event_card_slug = "letter-of-marque"
        game.event_cards = [event_card_slug]
        player = game.turn
        game.players_position[player] = Positions.TR1
        self.see_event_card_options(player, event_card_slug)
