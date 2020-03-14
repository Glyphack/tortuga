from datetime import timedelta

from fastapi import APIRouter
from pydantic.main import BaseModel

from jwt_helper import create_access_token
import config

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str


@router.post("/token", response_model=Token)
async def login_for_access_token(user: User):
    access_token_expires = timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
