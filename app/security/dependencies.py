from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import OAuth2PasswordBearer

from jose import jwt
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
        detail="Could not validate credentials"
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        raise credentials_exception

    return user

def require_dispatcher_or_admin(current_user):

    if current_user.role not in [
        "dispatcher",
        "admin"
    ]:

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return current_user