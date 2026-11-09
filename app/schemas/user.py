from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str | None = None
    password: str = Field(min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None
    role: str
    client_code: str | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"