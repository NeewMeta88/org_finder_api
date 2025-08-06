from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class OrganizationBase(BaseModel):
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    building_id: int
    activity_id: int


class OrganizationRead(OrganizationBase):
    id: int

    building_name: Optional[str] = None
    activity_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class OrganizationCreate(OrganizationBase):
    """Схема для создания новых организаций (если понадобится)"""
    pass
