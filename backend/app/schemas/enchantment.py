from pydantic import BaseModel, Field
from typing import List, Optional

class EnchantmentBase(BaseModel):
    name: str = Field(..., description="The enchantment's name")
    description: str = Field(..., description="Description of the enchantment effect")
    
class EnchantmentCreate(EnchantmentBase):
    pass

class EnchantmentResponse(EnchantmentBase):
    id: int = Field(..., description="The enchantment's unique identifier")
    
    class Config:
        from_attributes = True

# Representing an enchantment applied to an item
class ItemEnchantment(BaseModel):
    item_id: int = Field(..., description="The ID of the enchanted item")
    enchantment_id: int = Field(..., description="The ID of the enchantment applied")
    effect: str = Field(..., description="The specific effect for this item/enchantment combination")
    
    class Config:
        from_attributes = True