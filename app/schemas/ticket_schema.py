from pydantic import BaseModel


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

    address: AddressResponse | None = None

    class Config:

        from_attributes = True
