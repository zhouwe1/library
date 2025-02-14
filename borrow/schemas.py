from pydantic import BaseModel
from uuid import UUID

class BorrowingReq(BaseModel):
    detail_uuid: UUID
    user_id: int


class ReturningReq(BaseModel):
    detail_uuid: UUID
