from fastapi_utils.api_model import APIModel


class Token(APIModel):
    access_token: str
    token_type: str


class TokenData(APIModel):
    username: str = None


class User(APIModel):
    username: str


class VerifyTokenRequest(APIModel):
    token: str


class VerifyTokenResponse(APIModel):
    valid: bool
