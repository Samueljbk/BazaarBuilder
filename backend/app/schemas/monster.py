from pydantic import BaseModel, Field
from typing import List, Optional

class MonsterBase(BaseModel):
    name: str = Field(..., description="The monster's name")
    description: Optional[str] = Field(None, description="Description of the monster")
    appears_on_day: Optional[int] = Field(None, description="Day when the monster appears")
    
class MonsterCreate(MonsterBase):
    pass

class MonsterResponse(MonsterBase):
    id: int = Field(..., description="The monster's unique identifier")
    
    class Config:
        from_attributes = True