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
