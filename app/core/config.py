import os

from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(dotenv_path=os.path.join(BASEDIR, '../.env'))


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


API_V1_STR = "/api/v1"

SECRET_KEY = os.getenvb(b"SECRET_KEY")
print(SECRET_KEY)
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 10  # 60 minutes * 24 hours * 8 days = 8 days

BACKEND_CORS_ORIGINS = os.getenv(
    "BACKEND_CORS_ORIGINS"
)

SENTRY_DSN = os.getenv("SENTRY_DSN")
