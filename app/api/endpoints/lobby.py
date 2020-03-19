import uuid
from typing import Dict

from fastapi import APIRouter, Request, HTTPException
from app.api.services.game_service import create_new_game
from app.api.services.lobby_service import can_join_lobby
from app.schemas.auth import User
from app.schemas.lobby import (
    GetLobbyListResponse,
    Lobby,
    JoinLobbyResponse,
    JoinLobbyRequest,
    LeaveLobbyRequest,
    StartGameRequest,
    MyLobbyResponse,
    CreateLobbyResponse)

router = APIRouter()

lobbies: Dict[str, Lobby] = {}


@router.get("/lobby", response_model=GetLobbyListResponse)
async def get_lobbies_list(request: Request):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=401)
    return GetLobbyListResponse(lobbies=list(lobbies.values()))


@router.post("/lobby", response_model=CreateLobbyResponse)
async def create_lobby(request: Request):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=401)
    user = User(username=request.user.username)
    if not can_join_lobby(User(username=request.user.username), lobbies):
        raise HTTPException(status_code=400, detail="Already in a lobby")
    lobby_id = uuid.uuid4().hex[:6].upper()
    lobby = Lobby(
        id=lobby_id,
        size=9,
        occupy=1,
        host=user,
        players=[user],
    )
    lobbies[lobby_id] = lobby
    return CreateLobbyResponse(lobby=lobby)


@router.patch(
    "/lobby/join",
    response_model=JoinLobbyResponse)
async def join_lobby(request: Request, join_lobby_request: JoinLobbyRequest):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=401)
    if not can_join_lobby(User(username=request.user.username), lobbies):
        raise HTTPException(status_code=400, detail="Already in a lobby")
    lobby = lobbies.get(join_lobby_request.lobby_id)
    if not lobby:
        raise HTTPException(status_code=400, detail="Lobby does not exist")
    lobby.players.append(User(username=request.user.username))
    lobby.occupy += 1
    return JoinLobbyResponse(lobby=lobby, success=True)


@router.put("/lobby/leave")
async def leave_lobby(request: Request,
                      leave_lobby_request: LeaveLobbyRequest):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=401)
    lobby = lobbies.get(leave_lobby_request.lobby_id)
    if not lobby:
        raise HTTPException(status_code=400, detail="Lobby does not exist")
    user = User(username=request.user.username)
    if user not in lobby.players:
        raise HTTPException(status_code=400)
    lobby.players.remove(user)
    lobby.occupy -= 1


@router.post("/lobby/start")
async def start_game(request: Request, start_game_request: StartGameRequest):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=401)
    lobby = lobbies.get(start_game_request.lobby_id)
    if not lobby:
        raise HTTPException(status_code=400, detail="Lobby does not exist")
    user = User(username=request.user.username)
    if lobby.host != user:
        raise HTTPException(status_code=403,
                            detail="You cannot start this game")
    lobby.game_started = True
    create_new_game(lobby.id, lobby.players)


@router.get("/lobby/my-lobby", response_model=MyLobbyResponse)
async def my_lobby(request: Request):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=401)
    found_lobby = None
    can_start = False
    has_lobby = False
    user = User(username=request.user.username)
    for lobby in lobbies.values():
        if user in lobby.players:
            found_lobby = lobby
            can_start = user == lobby.host
            has_lobby = True
            break
    return MyLobbyResponse(
        lobby=found_lobby,
        can_start=can_start,
        has_lobby=has_lobby
    )
