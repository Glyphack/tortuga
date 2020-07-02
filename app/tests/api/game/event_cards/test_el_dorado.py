from app.schemas.game_schema import Action
from app.tests.api.game.base import BaseGameTestCase


class TestElDorado(BaseGameTestCase):
    def test_use_el_dorado_in_voting(self, game):
        game.event_cards = ["el-dorado"]
        player = game.turn
        self._reveal_event_card_action(player, 0)
        response = self._get_my_game(player).json()
        assert response["gameStatus"]["playerGameInfo"]["availableActions"] == [Action.ActionType.KEEP_EVENT_CARD]
        self._keep_event_card_action(player)
        game.turn = player
        self._call_for_an_attack(player)
        self._vote(player)
        self._vote(player)
        assert len(game.votes.participated_players) == 2
        print(game.last_action, game.votes)
