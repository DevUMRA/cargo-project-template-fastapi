from sqlalchemy import Column, Integer, String, Text, Boolean, CheckConstraint

from app.db.base import Base


class Location(Base):
    __tablename__ = "locations"

    __table_args__ = (
        CheckConstraint(
            "type IN ('foreign_warehouse', 'pickup_point')",
            name="ck_locations_type"
        ),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)

    type = Column(String(30), nullable=False)
    country = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(Text, nullable=False)
    contact_person = Column(String(100), nullable=False)
    phone = Column(String(30), nullable=False)
    instructions = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)