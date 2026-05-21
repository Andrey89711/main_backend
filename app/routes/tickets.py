from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.ticket import Ticket
from app.models.comment import Comment
from app.models.category import Category
from app.models.user_address import UserAddress

from app.schemas.ticket_schema import (
    TicketCreate,
    TicketResponse
)

from app.schemas.comment_schema import (
    CommentCreate,
    CommentResponse
)

from app.security.dependencies import (
    get_current_user,
    require_dispatcher
)


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_or_create_default_category(
    db: Session,
    category_id: int
):

    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if category:

        return category

    category = db.query(Category).filter(
        Category.name == "Общие заявки"
    ).first()

    if category:

        return category

    category = Category(
        name="Общие заявки"
    )

    db.add(category)

    db.flush()

    return category


@router.post(
    "/",
    response_model=TicketResponse
)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role in [
        "admin",
        "dispatcher"
    ]:

        raise HTTPException(
            status_code=403,
            detail="This role cannot create tickets"
        )

    category = get_or_create_default_category(
        db,
        ticket.category_id
    )

    address_link = db.query(UserAddress).filter(
        UserAddress.user_id == current_user.id,
        UserAddress.address_id == ticket.address_id,
        UserAddress.is_verified == True
    ).first()

    if not address_link:

        raise HTTPException(
            status_code=403,
            detail="Address is not verified or not linked to current user"
        )

    new_ticket = Ticket(
        description=ticket.description,
        category_id=category.id,
        address_id=ticket.address_id,
        resident_id=current_user.id,
        status="new",
        priority="medium"
    )

    db.add(new_ticket)

    db.commit()

    db.refresh(new_ticket)

    return new_ticket


@router.get(
    "/",
    response_model=list[TicketResponse]
)
def get_my_tickets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    tickets = db.query(Ticket).filter(
        Ticket.resident_id == current_user.id
    ).all()

    return tickets


@router.get(
    "/all",
    response_model=list[TicketResponse]
)
def get_all_tickets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    require_dispatcher(
        current_user
    )

    tickets = db.query(Ticket).all()

    return tickets


@router.patch(
    "/{ticket_id}/status"
)
def change_ticket_status(
    ticket_id: int,
    new_status: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    require_dispatcher(
        current_user
    )

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    ticket.status = new_status

    db.commit()

    return {
        "message": "Status updated"
    }


@router.get(
    "/{ticket_id}/comments",
    response_model=list[CommentResponse]
)
def get_comments(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    comments = db.query(Comment).filter(
        Comment.ticket_id == ticket_id
    ).all()

    return comments


@router.post(
    "/{ticket_id}/comments"
)
def add_comment(
    ticket_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    new_comment = Comment(
        text=comment.text,
        ticket_id=ticket_id,
        user_id=current_user.id
    )

    db.add(new_comment)

    db.commit()

    return {
        "message": "Comment added"
    }
