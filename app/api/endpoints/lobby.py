import uuid

from fastapi import APIRouter, Request, HTTPException
from app.schemas.auth import User
from app.schemas.lobby import GetLobbyListResponse, Lobby, JoinLobbyResponse, \
    JoinLobbyRequest, LeaveLobbyRequest

router = APIRouter()

lobbies = {}


@router.get("/lobby", response_model=GetLobbyListResponse)
async def get_lobbies_list(request: Request):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=401)
    return GetLobbyListResponse(lobbies=list(lobbies.values()))


@router.post("/lobby")
async def create_lobby(request: Request):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=401)
    user = User(username=request.user.username)
    for lobby in lobbies:
        if user in lobby.players:
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


@router.patch(
    "/lobby/{join_lobby_request.lobby_id}/join",
    response_model=JoinLobbyResponse)
async def join_lobby(request: Request, join_lobby_request: JoinLobbyRequest):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=401)
    lobby = lobbies.get(join_lobby_request.lobby_id)
    if not lobby:
        raise HTTPException(status_code=400, detail="Lobby does not exist")
    lobby.players.append(User(username=request.user.username))
    lobby.occupy += 1


@router.put("lobby/{leave_lobby_request.lobby_id}/leave")
async def leave_lobby(request: Request,
                      leave_lobby_request: LeaveLobbyRequest):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=401)
    lobby = lobbies.get(leave_lobby_request.lobby_id)
    if not lobby:
        raise HTTPException(status_code=400, detail="Lobby does not exist")
    user = User(username=request.user.username)
    if user not in lobby.platers:
        raise HTTPException(status_code=400)
    lobby.players.remove()
    lobby.occupy -= 1
