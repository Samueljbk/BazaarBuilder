from sqlalchemy import Column, Integer, String, Enum, Text
from sqlalchemy.orm import relationship
from ..database.database import Base
import enum

class MerchantType(enum.Enum):
    REGULAR = "regular"
    SKILL = "skill"
    LEVEL_UP = "level_up"
    DAY_SPECIFIC = "day_specific"

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    merchant_type = Column(Enum(MerchantType))
    appears_on_day = Column(Integer, nullable=True)