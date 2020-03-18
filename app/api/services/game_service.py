import random
from typing import List, Dict

from app.models.game import Game, Player
from app.schemas.auth import User

game_statuses: Dict[str, Game] = {}
players_game: Dict[str, str] = {}


def create_new_game(game_id: str, players: List[User]):
    players_info: Dict[str, Player] = {}
    players = [player.username for player in players]
    if len(players) // 2 != 0:
        dutch = random.choice(players)
        players.remove(dutch)
        dutch = Player(id=dutch, team=Player.Team.DUTCH.value)
        players_info[dutch.id] = dutch
        players_game[dutch.id] = game_id

    for index, player in enumerate(players):
        if index // 2 != 0:
            player_team = Player.Team.ENGLAND.value
        else:
            player_team = Player.Team.FRANCE.value
        players_info[player] = Player(id=player, team=player_team)
        players_game[player] = game_id

    new_game = Game(
        id=game_id,
        players=players,
        players_info=players_info,
        chests_position={},
        players_position={},
        last_action=None,
        is_over=False,
        turn=players[0],
        winner=None
    )
    game_statuses[game_id] = new_game


def get_player_game(username) -> Game:
    game_id = players_game.get(username)
    return game_statuses.get(game_id)


def get_player_info_in_game(game: Game, player_id: str) -> Player:
    return game.players_info[player_id]
