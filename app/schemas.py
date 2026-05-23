from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):
    pass

#basically create a base pydantic model class and for each specific niche usecase inherit that class and implement its own features


class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True