from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

from app.db.database import Base


class Ticket(Base):

    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    description = Column(Text, nullable=False)

    status = Column(String(50), default="new")

    priority = Column(String(50), default="medium")

    created_at = Column(DateTime, default=datetime.utcnow)

    resident_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )

    address_id = Column(
        Integer,
        ForeignKey("addresses.id")
    )

    address = relationship(
        "Address",
        back_populates="tickets"
    )

    resident = relationship("User")

    category = relationship("Category")
