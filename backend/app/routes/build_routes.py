from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..database.database import get_db
from ..schemas.build import (
    BuildCreate, 
    BuildResponse, 
    BuildUpdate, 
    BuildDetailedResponse
)
from ..models.build import Build, BuildItem, BuildSkill
from ..models.hero import Hero
from ..models.item import Item
from ..models.skill import Skill

router = APIRouter(
    prefix="/builds",
    tags=["builds"],
    responses={404: {"description": "Not found"}},
)

# Helper function to convert a Build model instance to a detailed response
def convert_build_to_detailed_response(build, db: Session):
    # Get hero name
    hero = db.query(Hero).filter(Hero.id == build.hero_id).first()
    hero_name = hero.name if hero else "Unknown"
    
    # Get detailed item information
    items = []
    for build_item in build.build_items:
        item = db.query(Item).filter(Item.id == build_item.item_id).first()
        if item:
            item_dict = {
                "id": item.id,
                "name": item.name,
                "description": item.description if hasattr(item, 'description') else "",
                "size": item.size.value if hasattr(item, 'size') and hasattr(item.size, 'value') else str(item.size) if hasattr(item, 'size') else "",
                "effect": item.effect if hasattr(item, 'effect') else "",
                "slot": build_item.slot
            }
            
            # Add optional attributes if they exist
            if hasattr(item, 'cooldown'):
                item_dict["cooldown"] = item.cooldown
            if hasattr(item, 'cost'):
                item_dict["cost"] = item.cost
                
            items.append(item_dict)
    
    # Get detailed skill information
    skills = []
    for build_skill in build.build_skills:
        skill = db.query(Skill).filter(Skill.id == build_skill.skill_id).first()
        if skill:
            skill_dict = {
                "id": skill.id,
                "name": skill.name
            }
            
            # Add optional attributes if they exist
            if hasattr(skill, 'description'):
                skill_dict["description"] = skill.description
            if hasattr(skill, 'effect'):
                skill_dict["effect"] = skill.effect
            if hasattr(skill, 'cooldown'):
                skill_dict["cooldown"] = skill.cooldown
            if hasattr(skill, 'cost'):
                skill_dict["cost"] = skill.cost
                
            skills.append(skill_dict)
    
    return {
        "id": build.id,
        "name": build.name,
        "description": build.description,
        "hero_id": build.hero_id,
        "hero_name": hero_name,
        "created_at": build.created_at,
        "updated_at": build.updated_at,
        "items": items,
        "skills": skills
    }

@router.post("/", response_model=BuildResponse, status_code=status.HTTP_201_CREATED)
async def create_build(build: BuildCreate, db: Session = Depends(get_db)):
    """
    Create a new build with items and skills.
    """
    # Check if hero exists
    hero = db.query(Hero).filter(Hero.id == build.hero_id).first()
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with ID {build.hero_id} not found"
        )
    
    # Create build
    db_build = Build(
        name=build.name,
        description=build.description,
        hero_id=build.hero_id
    )
    
    # Add items to build
    for item_data in build.build_items:
        # Check if item exists
        item = db.query(Item).filter(Item.id == item_data.item_id).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_data.item_id} not found"
            )
        
        # Create build item
        build_item = BuildItem(
            item_id=item_data.item_id,
            slot=item_data.slot
        )
        db_build.build_items.append(build_item)
    
    # Add skills to build
    for skill_data in build.build_skills:
        # Check if skill exists
        skill = db.query(Skill).filter(Skill.id == skill_data.skill_id).first()
        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Skill with ID {skill_data.skill_id} not found"
            )
        
        # Create build skill
        build_skill = BuildSkill(
            skill_id=skill_data.skill_id
        )
        db_build.build_skills.append(build_skill)
    
    # Save to database
    db.add(db_build)
    db.commit()
    db.refresh(db_build)
    
    return db_build

@router.get("/", response_model=List[BuildResponse])
async def get_builds(
    skip: int = 0, 
    limit: int = 100, 
    hero_id: Optional[int] = None,
    name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get a list of builds with optional filtering.
    """
    query = db.query(Build)
    
    # Apply filters if provided
    if hero_id:
        query = query.filter(Build.hero_id == hero_id)
    
    if name:
        query = query.filter(Build.name.ilike(f"%{name}%"))
    
    # Get builds
    builds = query.offset(skip).limit(limit).all()
    return builds

@router.get("/{build_id}", response_model=BuildDetailedResponse)
async def get_build(build_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific build.
    """
    build = db.query(Build).filter(Build.id == build_id).first()
    
    if not build:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Build with ID {build_id} not found"
        )
    
    return convert_build_to_detailed_response(build, db)

@router.put("/{build_id}", response_model=BuildResponse)
async def update_build(build_id: int, build_update: BuildUpdate, db: Session = Depends(get_db)):
    """
    Update a build.
    """
    # Get the existing build
    db_build = db.query(Build).filter(Build.id == build_id).first()
    
    if not db_build:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Build with ID {build_id} not found"
        )
    
    # Update basic build information
    if build_update.name is not None:
        db_build.name = build_update.name
        
    if build_update.description is not None:
        db_build.description = build_update.description
    
    # Update items if provided
    if build_update.build_items is not None:
        # Remove existing items
        for build_item in db_build.build_items:
            db.delete(build_item)
        
        # Add new items
        for item_data in build_update.build_items:
            # Check if item exists
            item = db.query(Item).filter(Item.id == item_data.item_id).first()
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Item with ID {item_data.item_id} not found"
                )
            
            # Create build item
            build_item = BuildItem(
                build_id=build_id,
                item_id=item_data.item_id,
                slot=item_data.slot
            )
            db.add(build_item)
    
    # Update skills if provided
    if build_update.build_skills is not None:
        # Remove existing skills
        for build_skill in db_build.build_skills:
            db.delete(build_skill)
        
        # Add new skills
        for skill_data in build_update.build_skills:
            # Check if skill exists
            skill = db.query(Skill).filter(Skill.id == skill_data.skill_id).first()
            if not skill:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Skill with ID {skill_data.skill_id} not found"
                )
            
            # Create build skill
            build_skill = BuildSkill(
                build_id=build_id,
                skill_id=skill_data.skill_id
            )
            db.add(build_skill)
    
    # Update the timestamp
    db_build.updated_at = datetime.utcnow()
    
    # Commit changes
    db.commit()
    db.refresh(db_build)
    
    return db_build

@router.delete("/{build_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_build(build_id: int, db: Session = Depends(get_db)):
    """
    Delete a build.
    """
    # Get the build
    build = db.query(Build).filter(Build.id == build_id).first()
    
    if not build:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Build with ID {build_id} not found"
        )
    
    # Delete the build (cascade will delete associated items and skills)
    db.delete(build)
    db.commit()
    
    return None