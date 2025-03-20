from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database.database import Base

class Enchantment(Base):
    __tablename__ = "enchantments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    
    # Relationships
    item_enchantments = relationship("ItemEnchantment", back_populates="enchantment")

class ItemEnchantment(Base):
    __tablename__ = "item_enchantments"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    enchantment_id = Column(Integer, ForeignKey("enchantments.id"))
    effect = Column(Text)
    
    # Relationships
    item = relationship("Item", back_populates="enchantments")
    enchantment = relationship("Enchantment", back_populates="item_enchantments")