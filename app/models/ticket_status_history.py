from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from app.db.database import Base


class TicketStatusHistory(Base):

    __tablename__ = "ticket_status_history"

    id = Column(Integer, primary_key=True)

    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id")
    )

    old_status = Column(String)

    new_status = Column(String)

    changed_by = Column(
        Integer,
        ForeignKey("users.id")
    )

    changed_at = Column(
        DateTime,
        default=datetime.utcnow
    )