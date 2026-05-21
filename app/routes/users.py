from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User
from app.models.address import Address

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

    address = current_user.address

    return {
        "id": current_user.id,
        "full_name":
            current_user.full_name,
        "email":
            current_user.email,
        "phone":
            current_user.phone,
        "street":
            address.street if address else "",
        "house":
            address.house if address else "",
        "apartment":
            address.apartment if address else ""
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

    if current_user.address is None:

        current_user.address = Address()

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
