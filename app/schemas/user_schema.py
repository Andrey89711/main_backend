from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class UserCreate(BaseModel):

    full_name: str

    email: EmailStr

    phone: str

    password: str = Field(
        min_length=6,
        max_length=72
    )

    role: str


class UserLogin(BaseModel):

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=72
    )