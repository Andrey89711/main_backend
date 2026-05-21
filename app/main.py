from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.db.database import Base
from app.db.database import SessionLocal

from app.models.role import Role
from app.models.user import User
from app.models.category import Category
from app.models.address import Address
from app.models.ticket import Ticket
from app.models.comment import Comment

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


Base.metadata.create_all(bind=engine)


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


@app.get("/")
def root():

    return {
        "message": "TSZH API"
    }
