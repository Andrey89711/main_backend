from pydantic import BaseModel


class CommentCreate(BaseModel):

    text: str


class CommentResponse(BaseModel):

    id: int

    text: str

    user_id: int

    class Config:

        from_attributes = True