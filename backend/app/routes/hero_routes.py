# app/routes/hero_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.database.database import get_db
from app.schemas.hero import HeroResponse, HeroCreate
from app.models.hero import Hero

router = APIRouter(
    prefix="/heroes",
    tags=["heroes"],
    responses={404: {"description": "Not found"}},
)

def convert_hero_for_response(hero: Hero) -> Dict[str, Any]:
    """Convert a Hero model instance to a dictionary suitable for response.
    
    Args:
        hero: Hero model instance
        
    Returns:
        Dictionary representation
    """
    hero_dict = {
        "id": hero.id,
        "name": hero.name,
    }
    return hero_dict

@router.get("/", response_model=List[HeroResponse])
async def get_heroes(
    skip: int = 0, 
    limit: int = 100, 
    name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get a list of heroes with optional filtering.
    """
    query = db.query(Hero)
    
    # Apply filters if provided
    if name:
        query = query.filter(Hero.name.ilike(f"%{name}%"))
    
    # Get heroes and convert them for response
    heroes = query.offset(skip).limit(limit).all()
    return [convert_hero_for_response(hero) for hero in heroes]

@router.get("/{hero_id}", response_model=HeroResponse)
async def get_hero(hero_id: int, db: Session = Depends(get_db)):
    """
    Get a specific hero by ID.
    """
    hero = db.query(Hero).filter(Hero.id == hero_id).first()
    if hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    return convert_hero_for_response(hero)

@router.get("/name/{hero_name}", response_model=HeroResponse)
async def get_hero_by_name(hero_name: str, db: Session = Depends(get_db)):
    """
    Get a specific hero by name.
    """
    hero = db.query(Hero).filter(Hero.name.ilike(f"%{hero_name}%")).first()
    if hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    return convert_hero_for_response(hero)

@router.post("/", response_model=HeroResponse)
async def create_hero(hero: HeroCreate, db: Session = Depends(get_db)):
    """
    Create a new hero.
    """
    # Check if a hero with the same name already exists
    existing_hero = db.query(Hero).filter(Hero.name == hero.name).first()
    if existing_hero:
        raise HTTPException(status_code=400, detail="Hero with this name already exists")
    
    db_hero = Hero(name=hero.name)
    
    db.add(db_hero)
    db.commit()
    db.refresh(db_hero)
    
    return convert_hero_for_response(db_hero)

@router.delete("/{hero_id}", response_model=HeroResponse)
async def delete_hero(hero_id: int, db: Session = Depends(get_db)):
    """
    Delete a hero.
    """
    hero = db.query(Hero).filter(Hero.id == hero_id).first()
    if hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    db.delete(hero)
    db.commit()
    
    return convert_hero_for_response(hero)