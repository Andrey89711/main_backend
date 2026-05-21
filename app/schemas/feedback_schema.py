from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class FeedbackAttachmentResponse(BaseModel):

    id: int

    file_name: str

    uploaded_at: datetime

    class Config:

        from_attributes = True


class FeedbackResponse(BaseModel):

    id: int

    ticket_id: int

    user_id: int

    author_name: str | None = None

    feedback_type: str

    feedback_type_label: str | None = None

    rating: int | None = None

    comment: str | None = None

    dispute_reason: str | None = None

    is_resolved: bool

    resolution_comment: str | None = None

    resolved_at: datetime | None = None

    created_at: datetime

    attachments: list[FeedbackAttachmentResponse] = []

    class Config:

        from_attributes = True


class FeedbackCreate(BaseModel):

    feedback_type: str = Field(
        ...,
        description="review | dispute"
    )

    rating: int | None = Field(
        default=None,
        ge=1,
        le=5
    )

    comment: str | None = None

    dispute_reason: str | None = None

    confirm_completion: bool = False


class DisputeResolveRequest(BaseModel):

    resolution_comment: str

    new_status: str = Field(
        default="in_progress",
        description="in_progress | completed | closed"
    )
