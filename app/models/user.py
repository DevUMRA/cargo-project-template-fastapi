from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, CheckConstraint, Index, func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(30), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="client")
    client_code = Column(String(30), unique=True, nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint("role IN ('client', 'employee', 'admin')",
                        name="ck_users_role"
                        ),
        Index(
            "uq_users_email_lower",
            func.lower(email),
            unique=True
        ),
    )



