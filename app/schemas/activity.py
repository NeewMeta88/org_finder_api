from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class ActivityRead(ActivityBase):
    id: int
    children: List['ActivityRead'] = []



    model_config = ConfigDict(from_attributes=True)


ActivityRead.update_forward_refs()
