from app.models.event_cards import EventCardsManager
from .base import BaseGameTestCase


class TestViewTwoEventCardsAction(BaseGameTestCase):
    def test_player_see_event_cards(self):
        response = self._view_two_event_cards_action(self.game.turn, [1, 2])
        assert response.status_code == 200
        response = self._get_my_game(self.game.turn).json()

        assert (
                len(response["gameStatus"]["playerGameInfo"][
                        "seenEventCards"]) == 2
        )

    def test_view_correct_cards(self):
        first_card = EventCardsManager.get(self.game.event_cards[0])
        second_card = EventCardsManager.get(self.game.event_cards[1])
        response = self._view_two_event_cards_action(self.game.turn, [1, 2])
        assert response.status_code == 200
        response = self._get_my_game(self.game.turn).json()

        assert (
                response["gameStatus"]["playerGameInfo"][
                    "seenEventCards"][0]["title"] == first_card.title
        )
        assert (
                response["gameStatus"]["playerGameInfo"][
                    "seenEventCards"][1]["title"] == second_card.title
        )