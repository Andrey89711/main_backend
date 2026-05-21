from sqlalchemy.orm import Session

from app.models.user_address import UserAddress
from app.security.dependencies import STAFF_ROLES


def clear_user_addresses(
    db: Session,
    user_id: int
):

    links = db.query(UserAddress).filter(
        UserAddress.user_id == user_id
    ).all()

    for link in links:
        db.delete(link)


def is_staff_role(role_code: str) -> bool:

    return role_code in STAFF_ROLES
