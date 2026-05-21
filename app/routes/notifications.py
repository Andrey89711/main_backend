from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.notification import Notification

from app.schemas.linked_ticket_schema import (
    NotificationResponse
)

from app.security.dependencies import get_current_user


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get(
    "/",
    response_model=list[NotificationResponse]
)
def get_my_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(
        Notification.created_at.desc()
    ).limit(100).all()


@router.patch(
    "/{notification_id}/read"
)
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()

    if not notification:

        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.is_read = True

    db.commit()

    return {
        "message": "Notification marked as read"
    }
