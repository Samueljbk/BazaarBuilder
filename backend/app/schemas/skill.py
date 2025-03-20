# app/schemas/skill.py

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class SkillSourceEnum(str, Enum):
    """Pydantic enum for skill sources."""
    UNIVERSAL = "universal"
    HERO_SPECIFIC = "hero_specific"
    MONSTER = "monster"

class SkillTierEnum(str, Enum):
    """Pydantic enum for skill tiers."""
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"

class SkillBase(BaseModel):
    """Base schema for skills."""
    name: str
    description: Optional[str] = None
    source: Optional[str] = None  # Changed from SkillSourceEnum to str
    hero_id: Optional[int] = None
    monster_id: Optional[int] = None
    tier: Optional[str] = None
    effect: Optional[str] = None
    types: Optional[str] = None

class SkillCreate(SkillBase):
    """Schema for creating a new skill."""
    pass

class Skill(SkillBase):
    """Schema for a skill with ID."""
    id: int

    class Config:
        """Pydantic config."""
        from_attributes = True
        
class SkillInDB(Skill):
    """Schema for a skill as stored in the database."""
    pass

# Define SkillResponse as an alias for Skill to maintain compatibility
SkillResponse = Skill