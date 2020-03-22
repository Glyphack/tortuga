from .base import BaseGameTestCase


class TestMyGame(BaseGameTestCase):
    def test_game_response_keys(self):
        player = self.game.get_jr_caption()
        response = self._get_my_game(player).json()
        assert all(
            x in response for
            x in ['gameId', 'gameStatus', 'hasGame']
        )

    def test_my_game_game_status(self):
        player = self.game.get_jr_caption()
        response = self._get_my_game(player).json()
        assert all(
            x in response["gameStatus"] for
            x in ["playersPosition",
                  "chestsPosition",
                  "playerGameInfo",
                  "lastAction",
                  "isOver",
                  "turn"
                  ]
        )

    def test_my_game_game_status_player_game_info(self):
        player = self.game.get_jr_caption()
        response = self._get_my_game(player).json()
        assert all(
            x in response["gameStatus"]["playerGameInfo"]
            for x in [
                "team",
                "voteCards",
                "eventCards",
                "role",
                "availableActions",
                "chests"
            ]
        )
