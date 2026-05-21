from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User

from app.security.dependencies import (
    get_current_user
)

from app.security.hashing import (
    hash_password
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
def get_profile(
    current_user: User = Depends(
        get_current_user
    )
):

    return {
        "id": current_user.id,
        "full_name":
            current_user.full_name,
        "email":
            current_user.email,
        "phone":
            current_user.phone,
        "street":
            current_user.address.street,
        "house":
            current_user.address.house,
        "apartment":
            current_user.address.apartment
    }


@router.put("/me")
def update_profile(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    current_user.full_name = (
        data["full_name"]
    )

    current_user.email = (
        data["email"]
    )

    current_user.phone = (
        data["phone"]
    )

    current_user.address.street = (
        data["street"]
    )

    current_user.address.house = (
        data["house"]
    )

    current_user.address.apartment = (
        data["apartment"]
    )

    if data.get("password"):

        current_user.password_hash = (
            hash_password(
                data["password"]
            )
        )

    db.commit()

    return {
        "message":
            "Profile updated"
    }