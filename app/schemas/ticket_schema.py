from datetime import datetime

from pydantic import BaseModel


class CategoryBrief(BaseModel):

    id: int

    name: str

    class Config:

        from_attributes = True


class AddressResponse(BaseModel):

    id: int

    street: str

    house: str

    apartment: str

    personal_account: str | None = None

    class Config:

        from_attributes = True


class TicketCreate(BaseModel):

    description: str

    category_id: int

    address_id: int


class TicketResponse(BaseModel):

    id: int

    description: str

    status: str

    priority: str

    resident_id: int

    category_id: int | None = None

    created_at: datetime | None = None

    subscribers_count: int = 0

    is_creator: bool = False

    is_linked: bool = False

    address: AddressResponse | None = None

    category: CategoryBrief | None = None

    class Config:

        from_attributes = True
