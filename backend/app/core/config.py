import os
from pathlib import Path
from typing import List

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings



VERSION = "0.0.1"
ROOT_PATH = Path(__file__).parent.parent.parent.parent
default_env_file_path = ROOT_PATH / ".env"
env_file_to_load = os.environ.get("ENV_FILE", str(default_env_file_path))

# env_file = os.environ.get("ENV_FILE") if "ENV_FILE" in os.environ else os.path.join(ROOT_PATH, ".env")

config = Config(env_file_to_load)

# ======= DATABASE ==========

MONGODB_URL: str = config("MONGODB_URL", default="mongodb://localhost:27017/")
MONGO_DATABASE: str = config("MONGO_DATABASE", default="clean-database")
MONGODB_MAX_CONNECTIONS_COUNT: int = config("MONGODB_MAX_CONNECTIONS_COUNT", cast=int, default=20)
MONGODB_MIN_CONNECTIONS_COUNT: int = config("MONGODB_MIN_CONNECTIONS_COUNT", cast=int, default=1)

MONGO_COLLECTION_USERS: str = config("MONGO_COLLECTION_USERS", default="users")


# =========== PROJECT ==========
PROJECT_NAME: str = config("PROJECT_NAME", default="Waterdip")
DEBUG: bool = config("DEBUG", cast=bool, default=False)
UNIT_TEST = config("UNIT_TEST", cast=bool, default=False)
DEPLOYMENT_ENV: str = config("DEPLOYMENT_ENV", default="local")
ALLOWED_HOSTS: List[str] = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="*")
AIO_CLIENT_TOUT_SEC: int = config("AIO_CLIENT_TOUT_SEC", cast=int, default=10)
LOG_LEVEL: str = config("LOG_LEVEL", default="INFO").upper()


# =========== SECURITY ==========
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=15)