from datetime import datetime, timedelta, UTC
import jwt
from app.core.config import settings

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError

password_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False

def create_access_token(user_id: int) -> str:
    now = datetime.now(UTC)

    expire= now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "iat": datetime.now(UTC),
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token