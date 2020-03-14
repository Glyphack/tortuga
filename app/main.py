from fastapi import FastAPI

from app.core import config
from app.api.api_v1 import api_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(api_router, prefix=config.API_V1_STR)
