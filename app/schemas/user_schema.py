from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class UserCreate(BaseModel):

    full_name: str

    email: EmailStr

    phone: str

    password: str = Field(
        min_length=5,
        max_length=72
    )

    street: str

    house: str

    apartment: str

    role: str = "resident"


class UserLogin(BaseModel):

    email: EmailStr

    password: str = Field(
        min_length=5,
        max_length=72
    )
