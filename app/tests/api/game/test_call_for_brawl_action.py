from app.schemas.game_schema import Positions
from .base import BaseGameTestCase


class TestCallForBrawlAction(BaseGameTestCase):
    def test_call_for_action_change_last_action(self):
        player = self.game.turn
        self.game.players_position[player] = Positions.TR1
        self._call_brawl_action(player)
        response = self._get_my_game(player).json()
        expected_last_action = {
            'actionType': 'call for brawl',
            'actionData': {
                'governor': player,
                'participatingPlayers': [player],
                'state': 'in_progress',
                "voteResults": []
            }
        }
        assert response["gameStatus"]["lastAction"] == expected_last_action

    def test_vote_completes_brawl(self):
        player = self.game.turn
        self.game.players_position[player] = Positions.TR1
        self.game.players_info[player].vote_cards[0].france = 10
        self._call_brawl_action(player)
        response = self._get_my_game(player).json()
        assert response["gameStatus"]["playerGameInfo"]["availableActions"] == ["vote"]
        self._vote(player)
        response = self._get_my_game(player).json()
        expected_last_action = {
            'actionType': 'call for brawl',
            'actionData': {
                'governor': player,
                'participatingPlayers': [],
                'state': 'success'
            }
        }

        assert len(
            response["gameStatus"]["lastAction"]["actionData"]["voteResults"]
        ) > 0
        del response["gameStatus"]["lastAction"]["actionData"]["voteResults"]
        assert response["gameStatus"]["lastAction"] == expected_last_action
        assert response["gameStatus"]["chestsPosition"]["tr_fr"] == 2
