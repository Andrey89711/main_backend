from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

from app.db.database import Base


class TicketFeedback(Base):

    __tablename__ = "ticket_feedback"

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

    feedback_type = Column(String(50), nullable=False)

    rating = Column(Integer, nullable=True)

    comment = Column(Text, nullable=True)

    dispute_reason = Column(Text, nullable=True)

    is_resolved = Column(Boolean, default=False, nullable=False)

    resolution_comment = Column(Text, nullable=True)

    resolved_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    resolved_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    ticket = relationship("Ticket", back_populates="feedback_entries")

    user = relationship("User", foreign_keys=[user_id])

    attachments = relationship(
        "TicketFeedbackAttachment",
        back_populates="feedback",
        cascade="all, delete-orphan"
    )


class TicketFeedbackAttachment(Base):

    __tablename__ = "ticket_feedback_attachments"

    id = Column(Integer, primary_key=True, index=True)

    feedback_id = Column(
        Integer,
        ForeignKey("ticket_feedback.id"),
        nullable=False,
        index=True
    )

    file_name = Column(String(255), nullable=False)

    stored_path = Column(String(500), nullable=False)

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    feedback = relationship(
        "TicketFeedback",
        back_populates="attachments"
    )
