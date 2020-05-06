from app.models.game import Game
from app.schemas.game_schema import Positions


def test_fill_empty_positions(game: Game):
    player = game.turn
    game.set_position(player, Positions.TR)
    assert (Positions.JR1 in game.players_position.values())
