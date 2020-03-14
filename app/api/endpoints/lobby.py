from fastapi import APIRouter

from app.schemas.auth import User
from app.schemas.lobby import GetLobbyListResponse, Lobby

router = APIRouter()


@router.get("/lobby", response_model=GetLobbyListResponse)
async def get_lobbies_list():
    dummy_lobby_1 = Lobby(id=1, size=5, occupy=1,
                          host=User(username="ez frost"),
                          players=[User(username="ez frost"),
                                   User(username="glyphack")])
    return GetLobbyListResponse(lobbies=[dummy_lobby_1])
