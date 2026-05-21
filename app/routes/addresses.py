from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.address import Address

from app.security.dependencies import (
    get_current_user
)


router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/")
def get_addresses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    addresses = db.query(Address).all()

    return addresses