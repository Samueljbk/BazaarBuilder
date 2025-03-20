from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class MerchantType(str, Enum):
    REGULAR = "regular"
    SKILL = "skill"
    LEVEL_UP = "level_up"
    DAY_SPECIFIC = "day_specific"

class MerchantBase(BaseModel):
    name: str = Field(..., description="The merchant's name")
    description: Optional[str] = Field(None, description="Description of the merchant")
    merchant_type: MerchantType = Field(..., description="Type of merchant")
    appears_on_day: Optional[int] = Field(None, description="Day when the merchant appears if day-specific")
    
class MerchantCreate(MerchantBase):
    pass

class MerchantResponse(MerchantBase):
    id: int = Field(..., description="The merchant's unique identifier")
    
    class Config:
        from_attributes = True