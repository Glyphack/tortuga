from typing import Dict

from app.schemas.auth import User
from app.schemas.lobby import Lobby


def can_join_lobby(user: User, lobbies: Dict[str, Lobby]):
    for lobby in lobbies.values():
        if user in lobby.players:
            return False

    return True
