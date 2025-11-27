from datetime import datetime, UTC, timedelta
from enum import Enum

from jose import jwt
from passlib.context import CryptContext

from src.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


def create_token(data: dict, days=1) -> tuple[str, int]:
    to_encode = data.copy()
    expire = (
        datetime.now(UTC)
        + timedelta(days=days)
    )
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encode_jwt, int(expire.timestamp())


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
