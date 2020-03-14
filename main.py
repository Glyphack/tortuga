from fastapi import FastAPI

import config
from authentication import router

app = FastAPI()

app.include_router(router, prefix=config.API_V1_STR)


@app.get("/")
def read_root():
    return {"Hello": "World"}
