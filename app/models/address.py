from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from app.db.database import Base


class Address(Base):

    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)

    street = Column(String)

    house = Column(String)

    apartment = Column(String)

    tickets = relationship(
        "Ticket",
        back_populates="address"
    )

    users = relationship("User")