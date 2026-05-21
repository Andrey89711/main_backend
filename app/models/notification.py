from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from app.db.database import Base


class Notification(Base):

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id"),
        nullable=True,
        index=True
    )

    channel = Column(
        String(20),
        default="web",
        nullable=False
    )

    title = Column(String(255), nullable=False)

    message = Column(Text, nullable=False)

    is_read = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
