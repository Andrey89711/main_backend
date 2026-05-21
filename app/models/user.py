from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from app.db.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(255), nullable=False)

    email = Column(String(255), unique=True, nullable=False)

    phone = Column(String(50))

    address_id = Column(
        Integer,
        ForeignKey("addresses.id")
    )

    address = relationship(
    "Address",
    back_populates="users"
    )

    password_hash = Column(String(255), nullable=False)

    role = Column(
        String(50),
        ForeignKey("roles.code"),
        nullable=False
    )

    role_info = relationship(
        "Role"
    )

    address_links = relationship(
        "UserAddress",
        back_populates="user"
    )

    is_active = Column(Boolean, default=True)
