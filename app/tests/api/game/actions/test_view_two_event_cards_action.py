from app.models.event_cards import EventCardsManager
from app.models.game import Game
from app.tests.api.game.base import BaseGameTestCase


class TestViewTwoEventCardsAction(BaseGameTestCase):
    def test_player_see_event_cards(self):
        player = self.game.turn
        response = self._view_two_event_cards_action(player, [0, 1])
        assert response.status_code == 200
        response = self._get_my_game(player).json()
        assert (
                len(response["gameStatus"]["playerGameInfo"][
                        "seenEventCards"]) == 2
        )

    def test_view_correct_cards(self):
        player = self.game.turn
        first_card = EventCardsManager.get(self.game.event_cards[0])
        second_card = EventCardsManager.get(self.game.event_cards[1])
        response = self._view_two_event_cards_action(player, [0, 1])
        assert response.status_code == 200
        response = self._get_my_game(player).json()

        assert (
                response["gameStatus"]["playerGameInfo"][
                    "seenEventCards"]["0"]["title"] == first_card.title
        )
        assert (
                response["gameStatus"]["playerGameInfo"][
                    "seenEventCards"]["1"]["title"] == second_card.title
        )

    def test_view_event_cards_change_turn(self, game: Game):
        player = game.turn
        response = self._view_two_event_cards_action(player, [0, 1])
        assert response.status_code == 200
        self._get_my_game(player).json()
        assert game.turn != player
