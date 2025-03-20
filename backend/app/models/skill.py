# app/models/skill.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
import enum

from app.database.database import Base

class SkillSource(enum.Enum):
    """Enumeration for skill sources."""
    UNIVERSAL = "universal"
    HERO_SPECIFIC = "hero_specific"
    MONSTER = "monster"

class SkillTier(enum.Enum):
    """Enumeration for skill tiers."""
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"

class Skill(Base):
    """SQLAlchemy model for skills."""
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    source = Column(Enum(SkillSource), default=SkillSource.UNIVERSAL)
    hero_id = Column(Integer, ForeignKey("heroes.id"), nullable=True)  # For hero-specific skills
    monster_id = Column(Integer, ForeignKey("monsters.id"), nullable=True)  # For monster-dropped skills
    tier = Column(String, nullable=True)  # Starting tier (Bronze, Silver, Gold)
    effect = Column(Text, nullable=True)  # Detailed effect description
    types = Column(String, nullable=True)  # Skill types (Crit, Buff, etc.)
    
    # Relationships
    hero = relationship("Hero", back_populates="skills")
    monster = relationship("Monster", back_populates="skills")