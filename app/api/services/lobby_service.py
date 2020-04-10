from typing import Dict

from app.schemas.auth import User
from app.schemas.lobby import Lobby

lobbies: Dict[str, Lobby] = {}


def can_join_lobby(user: User):
    for lobby in lobbies.values():
        if user in lobby.players:
            return False

    return True


def remove_lobby(lobby_id: str):
    del lobbies[lobby_id]


def leave_lobby(lobby_id: str, user: User):
    lobby = lobbies[lobby_id]
    lobby.players.remove(user)
    lobby.occupy -= 1
    if lobby.occupy == 0:
        remove_lobby(lobby.id)
