from app.models.game import Game
from app.schemas.game_schema import Action
from .base import BaseGameTestCase


class TestRevealEventCard(BaseGameTestCase):
    def test_reveal_card_with_no_option(self, game: Game):
        game.event_cards = ["spanish-armada"]
        player = game.turn
        self._reveal_event_card_action(player, 1)
        assert (
                game.last_action.action_type ==
                Action.ActionType.REVEAL_EVENT_CARD
        )
        assert game.turn != player

    def test_reveal_card_with_options(self, game: Game):
        game.event_cards = ["letter-of-marque"]
        player = game.turn
        self._reveal_event_card_action(player, 1)
        assert player == game.turn
        assert (
                game.last_action.action_data.can_keep ==
                True
        )


