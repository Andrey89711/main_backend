from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User
from app.models.address import Address
from app.models.role import Role

from app.security.dependencies import (
    get_current_user,
    require_admin
)

from app.security.hashing import (
    hash_password
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    require_admin(current_user)

    users = db.query(User).order_by(
        User.id
    ).all()

    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "role_name": user.role_info.name if user.role_info else user.role,
            "is_active": user.is_active,
            "is_current": user.id == current_user.id
        }
        for user in users
    ]


@router.get("/roles")
def get_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    require_admin(current_user)

    roles = db.query(Role).order_by(
        Role.name
    ).all()

    return [
        {
            "code": role.code,
            "name": role.name
        }
        for role in roles
    ]


@router.patch("/{user_id}/role")
def update_user_role(
    user_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    require_admin(current_user)

    if user_id == current_user.id:

        raise HTTPException(
            status_code=400,
            detail="Cannot change your own role"
        )

    role_code = data.get("role")

    role = db.query(Role).filter(
        Role.code == role_code
    ).first()

    if not role:

        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.role = role.code

    db.commit()

    return {
        "message": "Role updated"
    }


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

    user = db.query(User).filter(
        User.id == current_user.id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing_user = db.query(User).filter(
        User.email == data["email"],
        User.id != user.id
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    user.full_name = (
        data["full_name"]
    )

    user.email = (
        data["email"]
    )

    user.phone = (
        data["phone"]
    )

    if user.address is None:

        user.address = Address()

    user.address.street = (
        data["street"]
    )

    user.address.house = (
        data["house"]
    )

    user.address.apartment = (
        data["apartment"]
    )

    if data.get("password"):

        user.password_hash = (
            hash_password(
                data["password"]
            )
        )

    db.commit()

    return {
        "message":
            "Profile updated"
    }
