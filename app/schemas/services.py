from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ServiceCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class ServiceCategoryCreate(ServiceCategoryBase):
    pass

class ServiceCategoryOut(ServiceCategoryBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    services: List['ServiceOut'] = []

class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None

    class Config:
        orm_mode = True

class ServiceCreate(ServiceBase):
    category_id: int

class ServiceOut(ServiceBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    category: Optional[ServiceCategoryOut] = None
