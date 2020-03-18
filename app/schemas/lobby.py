from typing import List, Dict, Optional

from pydantic.main import BaseModel

from app.schemas.auth import User


class Lobby(BaseModel):
    id: str
    size: int
    occupy: int
    players: List[User]
    host: User
    game_started: bool = False


class GetLobbyListResponse(BaseModel):
    lobbies: List[Lobby]


class JoinLobbyRequest(BaseModel):
    lobby_id: str


class JoinLobbyResponse(BaseModel):
    success: bool
    lobby: Lobby


class MyLobbyResponse(BaseModel):
    lobby: Optional[Lobby]
    can_start: bool
    has_lobby: bool


class CreateLobbyResponse(BaseModel):
    lobby: Lobby


class LeaveLobbyRequest(BaseModel):
    lobby_id: str


class StartGameRequest(BaseModel):
    lobby_id: str
