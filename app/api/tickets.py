from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.ticket import Ticket

from app.models.ticket_status_history import TicketStatusHistory

from app.schemas.ticket_schema import TicketCreate

from app.security.dependencies import get_current_user

from app.security.dependencies import require_dispatcher_or_admin


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


@router.post("/")
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    new_ticket = Ticket(
        description=ticket.description,
        category_id=ticket.category_id,
        address_id=current_user.address_id,
        resident_id=current_user.id
    )

    db.add(new_ticket)

    db.commit()

    db.refresh(new_ticket)

    return new_ticket


@router.get("/")
def get_my_tickets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    tickets = db.query(Ticket).filter(
        Ticket.resident_id == current_user.id
    ).all()

    return tickets

@router.get("/all")
def get_all_tickets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    require_dispatcher_or_admin(
        current_user
    )

    tickets = db.query(Ticket).all()

    return tickets

@router.patch("/{ticket_id}/status")
def change_ticket_status(
    ticket_id: int,
    new_status: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    require_dispatcher_or_admin(
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

    old_status = ticket.status

    ticket.status = new_status

    history = TicketStatusHistory(
        ticket_id=ticket.id,
        old_status=old_status,
        new_status=new_status,
        changed_by=current_user.id
    )

    db.add(history)

    db.commit()

    return {
        "message": "Status updated"
    }