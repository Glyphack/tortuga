from datetime import timedelta

from fastapi import APIRouter, Response

from app.helpers.jwt_helper import create_access_token
from app.core import config
from app.schemas.auth import Token, User

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(user: User):
    access_token_expires = timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    ).decode("utf-8")

    return {"access_token": access_token, "token_type": "bearer"}
