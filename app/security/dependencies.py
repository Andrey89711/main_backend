from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import OAuth2PasswordBearer

from jose import jwt
from jose import ExpiredSignatureError
from jose import JWTError

from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.user import User

from app.security.jwt_handler import SECRET_KEY
from app.security.jwt_handler import ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    expired_exception = HTTPException(
        status_code=401,
        detail="Token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        subject = payload.get("sub")

        if subject is None:
            raise credentials_exception

    except ExpiredSignatureError:
        raise expired_exception

    except JWTError:
        raise credentials_exception

    user = None

    try:

        user_id = int(subject)

        user = db.query(User).filter(
            User.id == user_id
        ).first()

    except ValueError:

        user = db.query(User).filter(
            User.email == subject
        ).first()

    if user is None:
        raise credentials_exception

    return user

def require_dispatcher(current_user):

    if current_user.role != "dispatcher":

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return current_user


def require_dispatcher_or_admin(current_user):

    return require_dispatcher(current_user)


def require_admin(current_user):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return current_user


ROLES_WITH_ADDRESSES = frozenset({
    "resident",
})

STAFF_ROLES = frozenset({
    "dispatcher",
    "executor",
})


def require_resident_addresses(current_user):

    if current_user.role not in ROLES_WITH_ADDRESSES:

        raise HTTPException(
            status_code=403,
            detail="Addresses are not available for this role"
        )

    return current_user


def require_address_reviewer(current_user):

    if current_user.role not in [
        "admin",
        "dispatcher"
    ]:

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return current_user
