from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint

from sqlalchemy.orm import relationship

from datetime import datetime

from app.db.database import Base


class TicketLink(Base):

    __tablename__ = "ticket_links"

    __table_args__ = (
        UniqueConstraint(
            "ticket_id",
            "user_id",
            name="uq_ticket_links_ticket_user"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id"),
        nullable=False,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    joined_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    is_creator = Column(
        Boolean,
        default=False,
        nullable=False
    )

    ticket = relationship(
        "Ticket",
        back_populates="links"
    )

    user = relationship("User")
