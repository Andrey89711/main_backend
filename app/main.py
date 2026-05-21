from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.db.database import Base
from app.db.database import SessionLocal
from sqlalchemy import inspect
from sqlalchemy import text

from app.models.role import Role
from app.models.user import User
from app.models.category import Category
from app.models.address import Address
from app.models.ticket import Ticket
from app.models.comment import Comment
from app.models.user_address import UserAddress
from app.models.ticket_link import TicketLink
from app.models.notification import Notification
from app.models.ticket_action_log import TicketActionLog

from app.routes.users import router as users_router

from app.routes.addresses import (
    router as addresses_router
)

from app.models.ticket_status_history import (
    TicketStatusHistory
)

from app.routes.auth import router as auth_router

from app.routes.tickets import (
    router as tickets_router
)

from app.routes.notifications import (
    router as notifications_router
)


Base.metadata.create_all(bind=engine)


def ensure_schema_updates():

    inspector = inspect(engine)

    if inspector.has_table("addresses"):

        columns = {
            column["name"]
            for column in inspector.get_columns("addresses")
        }

        if "personal_account" not in columns:

            with engine.begin() as connection:

                connection.execute(
                    text(
                        "ALTER TABLE addresses "
                        "ADD COLUMN personal_account VARCHAR(100)"
                    )
                )

    if inspector.has_table("tickets"):

        ticket_columns = {
            column["name"]
            for column in inspector.get_columns("tickets")
        }

        if "merged_into_id" not in ticket_columns:

            with engine.begin() as connection:

                connection.execute(
                    text(
                        "ALTER TABLE tickets "
                        "ADD COLUMN merged_into_id INTEGER NULL"
                    )
                )


ensure_schema_updates()


def backfill_ticket_creator_links():

    db = SessionLocal()

    try:

        tickets = db.query(Ticket).all()

        for ticket in tickets:

            exists = db.query(TicketLink).filter(
                TicketLink.ticket_id == ticket.id,
                TicketLink.user_id == ticket.resident_id
            ).first()

            if not exists:

                db.add(
                    TicketLink(
                        ticket_id=ticket.id,
                        user_id=ticket.resident_id,
                        is_creator=True
                    )
                )

        db.commit()

    finally:

        db.close()


backfill_ticket_creator_links()


def seed_roles():

    roles = [
        {
            "code": "resident",
            "name": "Жилец"
        },
        {
            "code": "dispatcher",
            "name": "Диспетчер"
        },
        {
            "code": "admin",
            "name": "Администратор"
        },
        {
            "code": "executor",
            "name": "Исполнитель"
        }
    ]

    db = SessionLocal()

    try:

        for role in roles:

            exists = db.query(Role).filter(
                Role.code == role["code"]
            ).first()

            if not exists:

                db.add(
                    Role(**role)
                )

        db.commit()

    finally:

        db.close()


seed_roles()


def migrate_legacy_user_addresses():

    db = SessionLocal()

    try:

        users = db.query(User).filter(
            User.address_id.isnot(None)
        ).all()

        for user in users:

            exists = db.query(UserAddress).filter(
                UserAddress.user_id == user.id,
                UserAddress.address_id == user.address_id
            ).first()

            if not exists:

                db.add(
                    UserAddress(
                        user_id=user.id,
                        address_id=user.address_id,
                        is_primary=True,
                        is_verified=True
                    )
                )

        db.commit()

    finally:

        db.close()


migrate_legacy_user_addresses()

app = FastAPI(
    title="TSZH System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

app.include_router(tickets_router)

app.include_router(
    addresses_router
)

app.include_router(users_router)

app.include_router(notifications_router)


@app.get("/")
def root():

    return {
        "message": "TSZH API"
    }
