from sqlalchemy import Column
from sqlalchemy import String

from app.db.database import Base


class Role(Base):

    __tablename__ = "roles"

    code = Column(
        String(50),
        primary_key=True
    )

    name = Column(
        String(100),
        nullable=False,
        unique=True
    )
