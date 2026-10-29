
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    display_name: str | None = Field(default=None, max_length=150)


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    display_name: str | None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}



class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)
