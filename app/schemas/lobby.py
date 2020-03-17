from typing import List, Dict

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


class GetLobbyStatusResponse(BaseModel):
    lobby: Lobby


class CreateLobbyResponse(BaseModel):
    lobby: Lobby


class LeaveLobbyRequest(BaseModel):
    lobby_id: str


class StartGameRequest(BaseModel):
    lobby_id: str
