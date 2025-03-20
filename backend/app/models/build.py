from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.database import Base

class Build(Base):
    __tablename__ = "builds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    hero_id = Column(Integer, ForeignKey("heroes.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    hero = relationship("Hero", back_populates="builds")
    build_items = relationship("BuildItem", back_populates="build", cascade="all, delete-orphan")
    build_skills = relationship("BuildSkill", back_populates="build", cascade="all, delete-orphan")

class BuildItem(Base):
    __tablename__ = "build_items"

    id = Column(Integer, primary_key=True, index=True)
    build_id = Column(Integer, ForeignKey("builds.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    slot = Column(String, nullable=True)  # Optional positioning info for the UI

    # Relationships
    build = relationship("Build", back_populates="build_items")
    item = relationship("Item")

class BuildSkill(Base):
    __tablename__ = "build_skills"

    id = Column(Integer, primary_key=True, index=True)
    build_id = Column(Integer, ForeignKey("builds.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))

    # Relationships
    build = relationship("Build", back_populates="build_skills")
    skill = relationship("Skill")