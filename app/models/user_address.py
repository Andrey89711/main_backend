from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from sqlalchemy.orm import relationship

from app.db.database import Base


class UserAddress(Base):

    __tablename__ = "user_addresses"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    address_id = Column(
        Integer,
        ForeignKey("addresses.id"),
        nullable=False
    )

    is_primary = Column(Boolean, default=False)

    is_verified = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship(
        "User",
        back_populates="address_links"
    )

    address = relationship(
        "Address",
        back_populates="user_links"
    )
