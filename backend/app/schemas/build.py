from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Base schemas
class BuildItemBase(BaseModel):
    item_id: int
    slot: Optional[str] = None

class BuildSkillBase(BaseModel):
    skill_id: int

class BuildBase(BaseModel):
    name: str
    description: Optional[str] = None
    hero_id: int

# Create schemas (for input)
class BuildItemCreate(BuildItemBase):
    pass

class BuildSkillCreate(BuildSkillBase):
    pass

class BuildCreate(BuildBase):
    build_items: List[BuildItemCreate]
    build_skills: List[BuildSkillCreate]

# Read schemas (for output)
class BuildItemResponse(BuildItemBase):
    id: int
    build_id: int
    
    class Config:
        from_attributes = True  # Updated from orm_mode

class BuildSkillResponse(BuildSkillBase):
    id: int
    build_id: int
    
    class Config:
        from_attributes = True  # Updated from orm_mode

class BuildResponse(BuildBase):
    id: int
    created_at: datetime
    updated_at: datetime
    build_items: List[BuildItemResponse]
    build_skills: List[BuildSkillResponse]
    
    class Config:
        from_attributes = True  # Updated from orm_mode

# Additional schema with detailed item and skill info
class BuildDetailedResponse(BuildBase):
    id: int
    created_at: datetime
    updated_at: datetime
    hero_name: str
    items: List[dict]  # Will contain detailed item info
    skills: List[dict]  # Will contain detailed skill info
    
    class Config:
        from_attributes = True  # Updated from orm_mode

# Update schemas
class BuildItemUpdate(BuildItemBase):
    pass

class BuildSkillUpdate(BuildSkillBase):
    pass

class BuildUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    build_items: Optional[List[BuildItemCreate]] = None
    build_skills: Optional[List[BuildSkillCreate]] = None