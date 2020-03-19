import random
from typing import List, Dict

from app.models.game import Game, Player, Chests
from app.schemas.game import Positions
from app.schemas.auth import User

game_statuses: Dict[str, Game] = {}
players_game: Dict[str, str] = {}


def _generate_map(players: List[str]):
    players_position: Dict[str, Positions] = {}
    shuffled_players = players.copy()
    random.shuffle(shuffled_players)
    positions = [e.value for e in Positions]
    jr_head = 8
    fl_head = 0
    for index, player in enumerate(shuffled_players):
        if index % 2 == 0:
            players_position[player] = positions[jr_head]
            jr_head += 1
        else:
            players_position[player] = positions[fl_head]
            fl_head += 1
    return players_position


def _generate_chests_positions() -> Chests:
    chests = Chests(
        tr_en=1,
        tr_fr=1,
        sg=4,
        fd_en=0,
        fd_fr=0,
        jr_en=0,
        jr_fr=0
    )
    return chests


def _give_treasure_to_captains(players_info: Dict[str, Player],
                               positions: Dict[str, Positions]):
    updated_players_info = players_info.copy()
    for player, position in positions.items():
        if position == Positions.FL1.value or position == Positions.JR1.value:
            updated_players_info[player].chests += 1

    return updated_players_info


def create_new_game(game_id: str, players: List[User]):
    players_info: Dict[str, Player] = {}
    players = [player.username for player in players]
    players_copy = players.copy()
    random.shuffle(players_copy)
    if len(players_copy) // 2 != 0:
        dutch = players_copy[0]
        players_copy.remove(dutch)
        dutch = Player(id=dutch, team=Player.Team.DUTCH.value)
        players_info[dutch.id] = dutch
        players_game[dutch.id] = game_id

    for index, player in enumerate(players_copy):
        if index % 2 != 0:
            player_team = Player.Team.ENGLAND.value
        else:
            player_team = Player.Team.FRANCE.value
        players_info[player] = Player(id=player, team=player_team)
        players_game[player] = game_id

    players_positions = _generate_map(players)
    chests_position = _generate_chests_positions()
    players_info = _give_treasure_to_captains(players_info, players_positions)

    new_game = Game(
        id=game_id,
        players=players,
        players_info=players_info,
        chests_position=chests_position,
        players_position=players_positions,
        last_action=None,
        is_over=False,
        turn=players[0],
        winner=None
    )
    print(new_game)
    game_statuses[game_id] = new_game


users = ["first", "second", "third", "forth", "5", "6", "7", "8", "9"]
create_new_game("1", [User(username=username) for username in users])


def get_player_game(username) -> Game:
    game_id = players_game.get(username)
    return game_statuses.get(game_id)


def get_player_info_in_game(game: Game, player_id: str) -> Player:
    return game.players_info[player_id]
