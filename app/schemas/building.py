from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from app.schemas.organization import OrganizationRead

class BuildingBase(BaseModel):
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class BuildingRead(BuildingBase):
    id: int
    organizations: List[OrganizationRead] = []

    model_config = ConfigDict(from_attributes=True)
