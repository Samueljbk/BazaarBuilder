from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from ..database.database import Base

class Monster(Base):
    __tablename__ = "monsters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    appears_on_day = Column(Integer, nullable=True)
    
    # Relationships
    items = relationship("Item", back_populates="monster")
    skills = relationship("Skill", back_populates="monster")