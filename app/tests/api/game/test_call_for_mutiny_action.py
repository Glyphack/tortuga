from app.schemas.game_schema import Positions
from .base import BaseGameTestCase


class TestCallForMutiny(BaseGameTestCase):
    def test_call_for_mutiny_starts_voting(self):
        player = self.game.players[2]
        self.game.turn = player
        self._call_for_mutiny_action(player)
        response = self._get_my_game(player).json()
        assert response["gameStatus"]["lastAction"]["actionData"][
                   "participatingPlayers"] == [player]

    def test_voting_on_mutiny(self):
        player = self.game.players[2]
        self.game.turn = player
        self._call_for_mutiny_action(player)
        self._vote(player)
        response = self._get_my_game(player).json()
        assert (
                response["gameStatus"]["lastAction"]["actionData"]["state"] in
                ["success", "failed"]
        )

    def test_mutiny_success(self):
        captain = self.game.players[0]
        player = self.game.players[2]
        self.game.turn = player
        self._call_for_mutiny_action(player)
        self.game.players_info[player].vote_cards[0].skull += 1000
        self._vote(player)
        assert self.game.players_position[captain] == Positions.TR1
