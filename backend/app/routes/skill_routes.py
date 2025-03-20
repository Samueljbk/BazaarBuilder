# app/routes/skill_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import json

from app.database.database import get_db
from app.schemas.skill import Skill as SkillSchema, SkillCreate
from app.models.skill import Skill, SkillSource

router = APIRouter(
    prefix="/skills",
    tags=["skills"],
    responses={404: {"description": "Not found"}},
)

def convert_skill_for_response(skill: Skill) -> Dict[str, Any]:
    """Convert a Skill model instance to a dictionary suitable for response.
    
    Args:
        skill: Skill model instance
        
    Returns:
        Dictionary representation with string enum values
    """
    skill_dict = {
        "id": skill.id,
        "name": skill.name,
        "description": skill.description,
        "source": skill.source.value if skill.source else None,  # Convert enum to string
        "hero_id": skill.hero_id,
        "monster_id": skill.monster_id,
        "tier": skill.tier,
        "effect": skill.effect,
        "types": skill.types
    }
    return skill_dict

@router.get("/", response_model=List[SkillSchema])
async def get_skills(
    skip: int = 0, 
    limit: int = 100, 
    name: Optional[str] = None,
    hero_id: Optional[int] = None,
    source: Optional[str] = None,
    tier: Optional[str] = None,
    types: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get a list of skills with optional filtering.
    """
    query = db.query(Skill)
    
    # Apply filters if provided
    if name:
        query = query.filter(Skill.name.ilike(f"%{name}%"))
    if hero_id:
        query = query.filter(Skill.hero_id == hero_id)
    if source:
        try:
            source_enum = SkillSource(source)
            query = query.filter(Skill.source == source_enum)
        except ValueError:
            # Invalid source value, ignore this filter
            pass
    if tier:
        query = query.filter(Skill.tier == tier)
    if types:
        # Filter by any of the types in the comma-separated list
        type_list = [t.strip() for t in types.split(',')]
        conditions = []
        for t in type_list:
            conditions.append(Skill.types.ilike(f"%{t}%"))
        if conditions:
            from sqlalchemy import or_
            query = query.filter(or_(*conditions))
    
    # Get skills and convert them for response
    skills = query.offset(skip).limit(limit).all()
    return [convert_skill_for_response(skill) for skill in skills]

@router.get("/{skill_id}", response_model=SkillSchema)
async def get_skill(skill_id: int, db: Session = Depends(get_db)):
    """
    Get a specific skill by ID.
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    return convert_skill_for_response(skill)

@router.get("/hero/{hero_id}", response_model=List[SkillSchema])
async def get_skills_by_hero(hero_id: int, db: Session = Depends(get_db)):
    """
    Get all skills for a specific hero.
    """
    skills = db.query(Skill).filter(Skill.hero_id == hero_id).all()
    return [convert_skill_for_response(skill) for skill in skills]

@router.get("/tier/{tier}", response_model=List[SkillSchema])
async def get_skills_by_tier(tier: str, db: Session = Depends(get_db)):
    """
    Get all skills of a specific tier.
    """
    skills = db.query(Skill).filter(Skill.tier == tier).all()
    return [convert_skill_for_response(skill) for skill in skills]

@router.post("/", response_model=SkillSchema)
async def create_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    """
    Create a new skill.
    """
    try:
        source_enum = SkillSource(skill.source)
    except ValueError:
        source_enum = SkillSource.UNIVERSAL
        
    db_skill = Skill(
        name=skill.name,
        description=skill.description,
        source=source_enum,
        hero_id=skill.hero_id,
        monster_id=skill.monster_id,
        tier=skill.tier,
        effect=skill.effect,
        types=skill.types
    )
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    
    return convert_skill_for_response(db_skill)

@router.delete("/{skill_id}", response_model=SkillSchema)
async def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    """
    Delete a skill.
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    db.delete(skill)
    db.commit()
    
    return convert_skill_for_response(skill)