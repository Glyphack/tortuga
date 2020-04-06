from app.schemas.game_schema import Positions
from app.tests.api.game.base import BaseGameTestCase


class TestMaroonCrewAction(BaseGameTestCase):
    def test_maroon_crew_moves_player(self):
        previous_position = self.game.players_position.copy()
        player_to_maroon = self.game.players[2]
        response = self._maroon_crew(
            self.game.players[0],
            player_to_maroon
        )
        assert previous_position[player_to_maroon] != self.game.players_position[player_to_maroon]
        assert self.game.players_position[player_to_maroon] == Positions.TR1
