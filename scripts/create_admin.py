"""Создание ролей и учётной записи администратора."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.database import SessionLocal
from app.models import Address  # noqa: F401 — регистрация моделей
from app.models import Category  # noqa: F401
from app.models import Role
from app.models import Ticket  # noqa: F401
from app.models import User
from app.models import UserAddress  # noqa: F401
from app.security.hashing import hash_password


def main() -> None:

    email = "admin@example.com"
    password = "admin123"

    if len(sys.argv) >= 2:
        email = sys.argv[1]

    if len(sys.argv) >= 3:
        password = sys.argv[2]

    db = SessionLocal()

    try:

        roles = [
            ("admin", "Администратор"),
            ("resident", "Жилец"),
            ("dispatcher", "Диспетчер"),
            ("executor", "Исполнитель"),
        ]

        for code, name in roles:

            if not db.query(Role).filter(Role.code == code).first():

                db.add(Role(code=code, name=name))

        db.commit()

        if db.query(User).filter(User.email == email).first():

            print(f"Пользователь {email} уже существует")
            return

        db.add(
            User(
                full_name="Администратор",
                email=email,
                phone="",
                password_hash=hash_password(password),
                role="admin",
            )
        )

        db.commit()

        print("Администратор создан")
        print(f"  Email:    {email}")
        print(f"  Пароль:   {password}")

    finally:

        db.close()


if __name__ == "__main__":
    main()
