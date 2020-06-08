from app.schemas.game_schema import Action, Positions
from app.tests.api.game.base import BaseGameTestCase


class TestForceAnotherPlayerToChooseCard(BaseGameTestCase):
    def test_force_another_player_to_choose_card_works(self, game):
        game.event_cards = ["spanish-armada", "letter-of-marque", "black-spot"]
        player = game.turn
        other_player = game.players[1]
        event_cards_to_choose = [0, 1]
        self.force_another_player_to_choose_card(
            other_player, player, event_cards_to_choose
        )
        assert (
                game.last_action.action_type ==
                Action.ActionType.FORCE_ANOTHER_PLAYER_TO_CHOOSE_CARD
        )
        response = self._get_my_game(other_player).json()
        assert (
                response["gameStatus"]["playerGameInfo"]["availableActions"] ==
                [Action.ActionType.REVEAL_EVENT_CARD]
        )
        assert (
                response["gameStatus"]["eventCardsDeck"]["count"] == 2
        )
        assert (
                response["gameStatus"]["eventCardsDeck"]["selectableCards"] ==
                [0, 1]
        )

    def test_player_reveal_after_forced(self, game):
        game.event_cards = ["spanish-armada", "letter-of-marque", "black-spot"]
        player = game.turn
        other_player = game.players[1]
        event_cards_to_choose = [0, 2]
        self.force_another_player_to_choose_card(
            other_player, player, event_cards_to_choose
        )
        self._reveal_event_card_action(other_player, 1)
        assert game.players_position[other_player] in Positions.tr_positions()
