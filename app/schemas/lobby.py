from typing import List, Optional

from fastapi_utils.api_model import APIModel

from app.schemas.auth import User


class Lobby(APIModel):
    id: str
    size: int
    occupy: int
    players: List[User]
    host: User
    game_started: bool = False


class GetLobbyListResponse(APIModel):
    lobbies: List[Lobby]


class JoinLobbyRequest(APIModel):
    lobby_id: str


class JoinLobbyResponse(APIModel):
    success: bool
    lobby: Lobby


class MyLobbyResponse(APIModel):
    lobby: Optional[Lobby]
    can_start: bool
    has_lobby: bool


class CreateLobbyResponse(APIModel):
    lobby: Lobby


class LeaveLobbyRequest(APIModel):
    lobby_id: str


class StartGameRequest(APIModel):
    lobby_id: str
