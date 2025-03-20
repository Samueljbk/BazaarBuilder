from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database.database import Base

class Hero(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # Relationships
    items = relationship("Item", back_populates="hero")
    skills = relationship("Skill", back_populates="hero")
    builds = relationship("Build", back_populates="hero")