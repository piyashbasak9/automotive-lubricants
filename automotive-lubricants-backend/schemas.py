from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=4)
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    full_name: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    image: str

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3)
    category: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    image: str = Field(..., min_length=1)
