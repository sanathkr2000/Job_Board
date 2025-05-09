from pydantic import BaseModel
from typing import List
# --------------------------------------------------
# Pydantic Schema for Output (response) Model
# --------------------------------------------------



class UserData(BaseModel):
    id: int
    name: str
    email: str
    role: str


class UsersListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    users: List[UserData]


    class Config:
        orm_mode = True                    # Enables compatibility with ORM (like SQLAlchemy models)
        from_attributes = True
