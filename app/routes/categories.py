from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.category import Category

from app.schemas.category_schema import CategoryResponse

from app.security.dependencies import get_current_user


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get(
    "/",
    response_model=list[CategoryResponse]
)
def list_categories(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(Category).order_by(
        Category.id.asc()
    ).all()
