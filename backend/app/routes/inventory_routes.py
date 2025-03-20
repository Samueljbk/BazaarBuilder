from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from ..database.database import get_db
from ..models.build import Build, BuildItem, BuildSkill
from ..models.hero import Hero
from ..models.item import Item
from ..models.skill import Skill

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    responses={404: {"description": "Not found"}},
)

# Define schemas for inventory
class InventoryBase(BaseModel):
    hero_id: int
    item_ids: List[int]
    skill_ids: List[int]

class BuildMatchResponse(BaseModel):
    build_id: int
    build_name: str
    hero_id: int
    hero_name: str
    match_percentage: float
    missing_items: List[dict]
    missing_skills: List[dict]
    
    class Config:
        from_attributes = True  # Updated from orm_mode to fix warning

@router.post("/match-builds", response_model=List[BuildMatchResponse])
async def match_inventory_to_builds(
    inventory: InventoryBase,
    min_match_percentage: float = 0,
    db: Session = Depends(get_db)
):
    """
    Match current inventory against saved builds to find potential matches.
    Returns a list of builds sorted by match percentage.
    """
    # Validate hero
    hero = db.query(Hero).filter(Hero.id == inventory.hero_id).first()
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with ID {inventory.hero_id} not found"
        )
    
    # Get all builds for this hero
    builds = db.query(Build).filter(Build.hero_id == inventory.hero_id).all()
    
    # Calculate match percentage for each build
    results = []
    
    for build in builds:
        # Get all required items and skills for this build
        build_item_ids = [bi.item_id for bi in build.build_items]
        build_skill_ids = [bs.skill_id for bs in build.build_skills]
        
        # Count how many items and skills from the build are in the inventory
        matching_items = set(build_item_ids).intersection(set(inventory.item_ids))
        matching_skills = set(build_skill_ids).intersection(set(inventory.skill_ids))
        
        # Calculate match percentages
        if build_item_ids:
            item_match_percentage = len(matching_items) / len(build_item_ids) * 100
        else:
            item_match_percentage = 100  # No items required
            
        if build_skill_ids:
            skill_match_percentage = len(matching_skills) / len(build_skill_ids) * 100
        else:
            skill_match_percentage = 100  # No skills required
        
        # Calculate overall match percentage (weighted equally for now)
        match_percentage = (item_match_percentage + skill_match_percentage) / 2
        
        # Skip if match percentage is below threshold
        if match_percentage < min_match_percentage:
            continue
        
        # Get missing items
        missing_item_ids = set(build_item_ids) - set(inventory.item_ids)
        missing_items = []
        
        for item_id in missing_item_ids:
            item = db.query(Item).filter(Item.id == item_id).first()
            build_item = next((bi for bi in build.build_items if bi.item_id == item_id), None)
            
            if item:
                missing_items.append({
                    "id": item.id,
                    "name": item.name,
                    "slot": build_item.slot if build_item else None
                })
        
        # Get missing skills
        missing_skill_ids = set(build_skill_ids) - set(inventory.skill_ids)
        missing_skills = []
        
        for skill_id in missing_skill_ids:
            skill = db.query(Skill).filter(Skill.id == skill_id).first()
            
            if skill:
                missing_skills.append({
                    "id": skill.id,
                    "name": skill.name
                })
        
        # Add to results
        results.append({
            "build_id": build.id,
            "build_name": build.name,
            "hero_id": build.hero_id,
            "hero_name": hero.name,
            "match_percentage": round(match_percentage, 2),
            "missing_items": missing_items,
            "missing_skills": missing_skills
        })
    
    # Sort results by match percentage (highest first)
    results.sort(key=lambda x: x["match_percentage"], reverse=True)
    
    return results