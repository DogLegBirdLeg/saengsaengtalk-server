from pydantic import BaseModel
from datetime import datetime


class PostWriteModel(BaseModel):
    store_id: str
    place: str
    order_time: datetime
    min_member: int
    max_member: int
    order: dict


class PostUpdateModel(BaseModel):
    order_time: datetime
    place: str
    min_member: int
    max_member: int
