from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database.database import Base
import enum

class ItemSize(enum.Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class ItemSource(enum.Enum):
    HERO_SPECIFIC = "hero_specific"
    MONSTER = "monster"
    UNIVERSAL = "universal"

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    size = Column(Enum(ItemSize))
    source = Column(Enum(ItemSource))
    hero_id = Column(Integer, ForeignKey("heroes.id"), nullable=True)
    monster_id = Column(Integer, ForeignKey("monsters.id"), nullable=True)
    cooldown = Column(Integer, nullable=True)
    effect = Column(Text)
    cost = Column(Integer, nullable=True)
    
    # Relationships
    hero = relationship("Hero", back_populates="items")
    monster = relationship("Monster", back_populates="items")
    enchantments = relationship("ItemEnchantment", back_populates="item")