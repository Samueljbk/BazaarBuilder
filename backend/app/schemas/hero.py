# A simplified hero.py schema
from pydantic import BaseModel, Field
from typing import List, Optional

class HeroBase(BaseModel):
    name: str = Field(..., description="The hero's name")
    
class HeroCreate(HeroBase):
    pass

class HeroResponse(HeroBase):
    id: int = Field(..., description="The hero's unique identifier")
    
    class Config:
        from_attributes = True