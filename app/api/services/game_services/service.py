import random
from typing import List, Dict

from app.api.services.game_services.action_handlers import handlers
from app.api.services.game_services.action_handlers.action_handler import (
    ActionHandler
)
from app.api.services.lobby_service import remove_lobby
from app.models.game import Game, Player, Chests
from app.models import votes
from app.schemas import game_schema
from app.schemas.auth import User
from app.schemas.game_schema import PayloadType

game_statuses: Dict[str, Game] = {}
players_game: Dict[str, str] = {}


def _setup_vote_cards(game: Game):
    for player_info in game.players_info.values():
        if player_info.vote_cards is None:
            player_info.vote_cards = []
        for _ in range(0, 3):
            player_info.vote_cards.append(
                votes.generate_vote_card()
            )
    game.vote_deck = votes.generate_vote_card()


def _get_available_actions(player: Player, game: Game):
    available_actions = []
    player_position = game.players_position[player.id]
    if game.last_action:
        if game.last_action.action_type == game_schema.Action.ActionType.CALL_FOR_AN_ATTACK:
            if player.id in game.last_action.action_data.participating_players:
                available_actions = [game_schema.Action.ActionType.VOTE]
                return available_actions
            if (
                    player.id == game.last_action.action_data.which_captain and
                    game.last_action.action_data.state == game_schema.State.Success
            ):
                available_actions = [game_schema.Action.ActionType.PUT_CHEST]
                return available_actions
        if game.last_action.action_type == game_schema.Action.ActionType.CALL_FOR_BRAWL:
            if player.id in game.last_action.action_data.participating_players:
                available_actions = [game_schema.Action.ActionType.VOTE]
                return available_actions
        if game.last_action.action_type == game_schema.Action.ActionType.CALL_FOR_A_MUTINY:
            if player.id in game.last_action.action_data.participating_players:
                available_actions = [game_schema.Action.ActionType.VOTE]
                return available_actions
    if player.id != game.turn:
        return available_actions
    if player.chests > 0:
        available_actions = [game_schema.Action.ActionType.PUT_CHEST]
        return available_actions
    global_actions = [
        game_schema.Action.ActionType.MOVE,
        game_schema.Action.ActionType.VIEW_TWO_EVENT_CARDS,
        game_schema.Action.ActionType.REVEAL_ONE_EVENT_CARD,
        game_schema.Action.ActionType.FORCE_ANOTHER_PLAYER_TO_CHOOSE_CARD,
        game_schema.Action.ActionType.CALL_FOR_A_MUTINY
    ]
    available_actions.extend(global_actions)
    if player_position in [
        game_schema.Positions.FD1, game_schema.Positions.JR1
    ]:
        available_actions.extend([
            game_schema.Action.ActionType.CALL_FOR_AN_ATTACK,
            game_schema.Action.ActionType.MAROON_ANY_CREW_MATE_TO_TORTUGA,
            game_schema.Action.ActionType.MOVE_TREASURE
        ])
    if player_position == game_schema.Positions.TR1:
        available_actions.append(
            game_schema.Action.ActionType.CALL_FOR_BRAWL
        )
    return available_actions


def _generate_map(players: List[str]):
    players_position: Dict[str, game_schema.Positions] = {}
    shuffled_players = players.copy()
    random.shuffle(shuffled_players)
    positions = [e.value for e in game_schema.Positions]
    jr_head = 10
    fd_head = 1
    for index, player in enumerate(shuffled_players):
        if index % 2 == 0:
            players_position[player] = positions[jr_head]
            jr_head += 1
        else:
            players_position[player] = positions[fd_head]
            fd_head += 1
    return players_position


def _generate_chests_positions() -> Chests:
    chests = Chests(
        tr_en=1,
        tr_fr=1,
        sg_nt=4,
        fd_en=0,
        fd_fr=0,
        jr_en=0,
        jr_fr=0
    )
    return chests


def _give_treasure_to_captains(players_info: Dict[str, Player],
                               positions: Dict[str, game_schema.Positions]):
    updated_players_info = players_info.copy()
    for player, position in positions.items():
        if (
                position == game_schema.Positions.FD1.value or
                position == game_schema.Positions.JR1.value
        ):
            updated_players_info[player].chests += 1

    return updated_players_info


def create_new_game(game_id: str, players: List[str], host: str) -> Game:
    players_info: Dict[str, Player] = {}
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
        players_info=players_info,
        chests_position=chests_position,
        players_position=players_positions,
        last_action=None,
        is_over=False,
        winner=None,
        host=host,
    )
    _setup_vote_cards(new_game)
    new_game.turn = new_game.get_jr_caption()
    game_statuses[game_id] = new_game
    return new_game


def get_player_game(username) -> Game:
    game_id = players_game.get(username)
    return game_statuses.get(game_id)


def get_player_info_in_game(game: Game, player_id: str) -> Player:
    return game.players_info[player_id]


def remove_game(game_id: str):
    del game_statuses[game_id]
    remove_lobby(game_id)


def is_game_host(game: Game, player: str):
    return game.host == player


def generate_game_schema_from_game(username: str):
    game = get_player_game(username)
    player_info = get_player_info_in_game(game, username)
    return game_schema.GameStatus(
        players_position=game.players_position,
        chests_position=game_schema.Chests(
            tr_en=game.chests_position.tr_en,
            tr_fr=game.chests_position.tr_fr,
            fd_fr=game.chests_position.fd_fr,
            fd_en=game.chests_position.fd_en,
            jr_fr=game.chests_position.jr_fr,
            jr_en=game.chests_position.jr_en,
            sg_nt=game.chests_position.sg_nt,
        ),
        player_game_info=game_schema.PlayerGameInfo(
            team=player_info.team,
            vote_cards=player_info.vote_cards,
            event_cards=player_info.event_cards,
            role=None,
            available_actions=_get_available_actions(player_info, game),
            chests=player_info.chests
        ),
        last_action=game.last_action,
        is_over=game.is_over,
        turn=User(username=game.turn),
        winner=game.winner,
    )


def get_action_handler(game: Game, player: str,
                       action: game_schema.Action,
                       payload: PayloadType = None) -> ActionHandler:
    action_handler_class = handlers.get(action.action_type)
    action_handler = action_handler_class(game, player, action, payload)
    return action_handler
