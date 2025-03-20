from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from .enchantment import EnchantmentResponse  # Import the EnchantmentResponse

class ItemSize(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class ItemSource(str, Enum):
    HERO_SPECIFIC = "hero_specific"
    MONSTER = "monster"
    UNIVERSAL = "universal"

class ItemBase(BaseModel):
    name: str = Field(..., description="The item's name")
    description: str = Field(..., description="Description of the item effect")
    size: ItemSize = Field(..., description="Size of the item (small, medium, large)")
    source: ItemSource = Field(..., description="Source of the item (hero-specific, monster, universal)")
    hero_id: Optional[int] = Field(None, description="ID of the hero if item is hero-specific")
    monster_id: Optional[int] = Field(None, description="ID of the monster if item is monster-specific")
    cooldown: Optional[int] = Field(None, description="Cooldown of the item in turns")
    effect: str = Field(..., description="Effect of the item when used")
    cost: Optional[int] = Field(None, description="Cost to purchase the item if available from merchant")
    
class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int = Field(..., description="The item's unique identifier")
    enchantments: List[EnchantmentResponse] = Field(default_factory=list, description="Enchantments applied to this item")
    
    class Config:
        from_attributes = True