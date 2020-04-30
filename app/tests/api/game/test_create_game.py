import pytest

from app.api.services.game_services.service import create_new_game
from app.models.game import Game
from app.schemas.game_schema import Team


@pytest.fixture
def game_creator():
    def _game_creator(size, game_id="x"):
        players = list(map(str, range(size)))
        return create_new_game(game_id, players, players[0])

    return _game_creator


def test_create_game_correct_teams(game_creator):
    for i in range(1, 10):
        game: Game = game_creator(size=i)
        has_dutch = i % 2 != 0
        britain_players_count = 0
        france_players_count = 0
        dutch_count = 0
        for info in game.players_info.values():
            if info.team == Team.BRITAIN:
                britain_players_count += 1
            elif info.team == Team.FRANCE:
                france_players_count += 1
            else:
                assert has_dutch is True
                dutch_count += 1
