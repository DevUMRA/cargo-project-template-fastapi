from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserRegister, UserResponse, UserLogin,TokenResponse
from app.auth.service import register_user, authenticate_user

from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    try:
        return register_user(db, user_data)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        ) from error

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db,
        user_data.email,
        user_data.password
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email немесе құпиясөз қате",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(user.id)

    return TokenResponse(
        access_token=access_token
    )