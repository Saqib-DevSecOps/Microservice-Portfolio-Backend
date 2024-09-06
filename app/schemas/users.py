# Pydantic models for data validation and serialization
from pydantic import BaseModel, EmailStr
from typing import Optional

from sqlalchemy import DateTime


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: Optional[DateTime] = None
    updated_at: Optional[DateTime] = None