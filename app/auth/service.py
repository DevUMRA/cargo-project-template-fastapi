from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserRegister
from app.core.security import hash_password, verify_password

from sqlalchemy.exc import IntegrityError

def get_user_by_email(db: Session, email: str) -> User | None:
    statement = select(User).where(
        func.lower(User.email) == email.lower()
    )

    return db.scalar(statement)

def register_user(db: Session, user_data: UserRegister) -> User:
    existing_user = get_user_by_email(db, user_data.email)

    if existing_user is not None:
        raise ValueError("Бұл email бұрын тіркелген")

    hashed_password = hash_password(user_data.password)

    new_user = User(
        name=user_data.name,
        email=user_data.email.strip().lower(),
        phone=user_data.phone,
        password_hash=hashed_password,
        role="client",
        is_active=True
    )

    try:
        db.add(new_user)
        db.flush()

        new_user.client_code = f"CL-{new_user.id:06d}"

        db.commit()

    except IntegrityError:
        db.rollback()
        raise ValueError("Email немесе клиент коды қайталанған")

    db.refresh(new_user)
    return new_user

def authenticate_user(
    db: Session,
    email: str,
    password: str
) -> User | None:

    user = get_user_by_email(db, email)

    if user is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    if not user.is_active:
        return None

    return user

