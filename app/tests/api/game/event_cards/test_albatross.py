from app.models.game import Game
from app.schemas.game_schema import Action
from app.tests.api.game.base import BaseGameTestCase


class TestAlbatross(BaseGameTestCase):
    def test_reveal_albatross_card(self, game: Game):
        game.event_cards = ["albatross"]
        player = game.turn
        self._reveal_event_card_action(player, 0)
        game_status = self._get_my_game(player).json()
        assert (
                game_status
                ["gameStatus"]
                ["playerGameInfo"]
                ["availableActions"] == [Action.ActionType.KEEP_EVENT_CARD]
        )
