from fastapi import FastAPI

from app.core import config
from app.api.endpoints.auth import router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(router, prefix=config.API_V1_STR)
