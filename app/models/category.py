from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.db.database import Base


class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False, unique=True)
