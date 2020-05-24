from app.models.game import Game
from app.schemas.game_schema import Action, Positions
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

    def test_two_players_with_albatross(self, game: Game):
        game.event_cards = ["albatross", "albatross"]
        player1 = game.turn
        self._reveal_event_card_action(player1, 0)
        self._keep_event_card_action(player1)
        while game.get_position(game.turn) not in Positions.jr_positions():
            game.next_turn()
        player2 = game.turn
        self._reveal_event_card_action(player2, 0)
        self._keep_event_card_action(player2)
        response = self._get_my_game(player2).json()
        assert (
                response["gameStatus"]["playersPosition"][
                    player1] in Positions.tr_positions()
        )
        assert (
                response["gameStatus"]["playersPosition"][
                    player2] in Positions.tr_positions()
        )
