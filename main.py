from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.core import config
from app.api.api_v1 import api_router
from app.middlewares.authentication import JWTAuthenticationBackend

app = FastAPI()

# CORS
origins = []

# Set all CORS enabled origins
if config.BACKEND_CORS_ORIGINS:
    origins_raw = config.BACKEND_CORS_ORIGINS.split(",")
    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),

app.add_middleware(
    AuthenticationMiddleware, backend=JWTAuthenticationBackend()
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(api_router, prefix=config.API_V1_STR)
