# app/routes/item_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.database.database import get_db
from app.schemas.item import ItemResponse, ItemCreate, ItemSize, ItemSource
from app.models.item import Item, ItemSize as ItemSizeModel, ItemSource as ItemSourceModel

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

def convert_item_for_response(item: Item) -> Dict[str, Any]:
    """Convert an Item model instance to a dictionary suitable for response.
    
    Args:
        item: Item model instance
        
    Returns:
        Dictionary representation with string enum values
    """
    item_dict = {
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "size": item.size.value if item.size else None,  # Convert enum to string
        "source": item.source.value if item.source else None,  # Convert enum to string
        "hero_id": item.hero_id,
        "monster_id": item.monster_id,
        "cooldown": item.cooldown,
        "effect": item.effect,
        "cost": item.cost,
        "enchantments": []  # We'll leave this empty for now as it's complex to load
    }
    return item_dict

@router.get("/", response_model=List[ItemResponse])
async def get_items(
    skip: int = 0, 
    limit: int = 100, 
    name: Optional[str] = None,
    size: Optional[str] = None,
    source: Optional[str] = None,
    hero_id: Optional[int] = None,
    monster_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get a list of items with optional filtering.
    """
    query = db.query(Item)
    
    # Apply filters if provided
    if name:
        query = query.filter(Item.name.ilike(f"%{name}%"))
    if size:
        try:
            size_enum = ItemSizeModel(size)
            query = query.filter(Item.size == size_enum)
        except ValueError:
            # Invalid size value, ignore this filter
            pass
    if source:
        try:
            source_enum = ItemSourceModel(source)
            query = query.filter(Item.source == source_enum)
        except ValueError:
            # Invalid source value, ignore this filter
            pass
    if hero_id:
        query = query.filter(Item.hero_id == hero_id)
    if monster_id:
        query = query.filter(Item.monster_id == monster_id)
    
    # Get items and convert them for response
    items = query.offset(skip).limit(limit).all()
    return [convert_item_for_response(item) for item in items]

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get a specific item by ID.
    """
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return convert_item_for_response(item)

@router.get("/hero/{hero_id}", response_model=List[ItemResponse])
async def get_items_by_hero(hero_id: int, db: Session = Depends(get_db)):
    """
    Get all items for a specific hero.
    """
    items = db.query(Item).filter(Item.hero_id == hero_id).all()
    return [convert_item_for_response(item) for item in items]

@router.get("/size/{size}", response_model=List[ItemResponse])
async def get_items_by_size(size: str, db: Session = Depends(get_db)):
    """
    Get all items of a specific size.
    """
    try:
        size_enum = ItemSizeModel(size)
        items = db.query(Item).filter(Item.size == size_enum).all()
        return [convert_item_for_response(item) for item in items]
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid size value: {size}")

@router.get("/source/{source}", response_model=List[ItemResponse])
async def get_items_by_source(source: str, db: Session = Depends(get_db)):
    """
    Get all items from a specific source.
    """
    try:
        source_enum = ItemSourceModel(source)
        items = db.query(Item).filter(Item.source == source_enum).all()
        return [convert_item_for_response(item) for item in items]
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid source value: {source}")

@router.post("/", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new item.
    """
    try:
        size_enum = ItemSizeModel(item.size)
        source_enum = ItemSourceModel(item.source)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid enum value: {str(e)}")
        
    db_item = Item(
        name=item.name,
        description=item.description,
        size=size_enum,
        source=source_enum,
        hero_id=item.hero_id,
        monster_id=item.monster_id,
        cooldown=item.cooldown,
        effect=item.effect,
        cost=item.cost
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return convert_item_for_response(db_item)

@router.delete("/{item_id}", response_model=ItemResponse)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete an item.
    """
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    
    return convert_item_for_response(item)