from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.db.database import SessionLocal

from app.models.ticket import Ticket
from app.models.ticket_feedback import TicketFeedback

from app.schemas.feedback_schema import (
    DisputeResolveRequest,
    FeedbackCreate,
    FeedbackResponse,
)

from app.schemas.ticket_schema import TicketResponse

from app.security.dependencies import (
    get_current_user,
    require_dispatcher
)

from app.services import linked_tickets as linked_service
from app.services import feedback_service


router = APIRouter(
    prefix="/tickets",
    tags=["Feedback"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get(
    "/disputed",
    response_model=list[TicketResponse]
)
def list_disputed_tickets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    require_dispatcher(current_user)

    from app.routes.tickets import build_ticket_response

    tickets = db.query(Ticket).filter(
        Ticket.status == "dispute_review"
    ).order_by(
        Ticket.created_at.desc()
    ).all()

    return [
        build_ticket_response(db, ticket, current_user)
        for ticket in tickets
    ]


@router.get(
    "/{ticket_id}/feedback",
    response_model=list[FeedbackResponse]
)
def list_ticket_feedback(
    ticket_id: int,
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

    if current_user.role not in ["dispatcher", "admin"]:

        if not linked_service.user_has_ticket_access(
            db,
            ticket,
            current_user
        ):

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

    entries = db.query(TicketFeedback).options(
        joinedload(TicketFeedback.attachments)
    ).filter(
        TicketFeedback.ticket_id == ticket_id
    ).order_by(
        TicketFeedback.created_at.desc()
    ).all()

    return [
        feedback_service.build_feedback_response(db, entry)
        for entry in entries
    ]


@router.get(
    "/{ticket_id}/feedback/can-submit"
)
def can_submit_feedback(
    ticket_id: int,
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

    return {
        "can_submit": feedback_service.user_can_leave_feedback(
            db,
            ticket,
            current_user
        ),
        "has_active_dispute": feedback_service.has_active_dispute(
            db,
            ticket_id
        ),
        "status": ticket.status
    }


@router.post(
    "/{ticket_id}/feedback",
    response_model=FeedbackResponse
)
async def create_ticket_feedback(
    ticket_id: int,
    feedback_type: Annotated[str, Form()],
    rating: Annotated[int | None, Form()] = None,
    comment: Annotated[str | None, Form()] = None,
    dispute_reason: Annotated[str | None, Form()] = None,
    confirm_completion: Annotated[bool, Form()] = False,
    files: list[UploadFile] = File(default=[]),
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

    feedback = feedback_service.create_feedback(
        db,
        ticket=ticket,
        user=current_user,
        feedback_type=feedback_type,
        rating=rating,
        comment=comment,
        dispute_reason=dispute_reason,
        confirm_completion=confirm_completion
    )

    if feedback_type == "dispute" and files:

        await feedback_service.save_attachments(
            db,
            feedback=feedback,
            files=files
        )

    db.commit()
    db.refresh(feedback)

    feedback = db.query(TicketFeedback).options(
        joinedload(TicketFeedback.attachments)
    ).filter(
        TicketFeedback.id == feedback.id
    ).first()

    return feedback_service.build_feedback_response(
        db,
        feedback
    )


@router.post(
    "/{ticket_id}/feedback/json",
    response_model=FeedbackResponse
)
def create_ticket_feedback_json(
    ticket_id: int,
    payload: FeedbackCreate,
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

    feedback = feedback_service.create_feedback(
        db,
        ticket=ticket,
        user=current_user,
        feedback_type=payload.feedback_type,
        rating=payload.rating,
        comment=payload.comment,
        dispute_reason=payload.dispute_reason,
        confirm_completion=payload.confirm_completion
    )

    db.commit()
    db.refresh(feedback)

    return feedback_service.build_feedback_response(
        db,
        feedback
    )


@router.patch(
    "/{ticket_id}/dispute/resolve"
)
def resolve_ticket_dispute(
    ticket_id: int,
    payload: DisputeResolveRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    require_dispatcher(current_user)

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    feedback_service.resolve_dispute(
        db,
        ticket=ticket,
        dispatcher=current_user,
        resolution_comment=payload.resolution_comment,
        new_status=payload.new_status
    )

    db.commit()

    return {
        "message": "Dispute resolved",
        "status": ticket.status
    }
