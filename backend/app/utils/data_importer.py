# app/utils/data_importer.py

import json
import logging
import sys
import os
from typing import List, Dict, Any
from sqlalchemy.orm import Session

# Add the parent directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# Now use absolute imports
from app.database.database import SessionLocal, engine
from app.models.hero import Hero
from app.models.item import Item, ItemSize, ItemSource
from app.models.skill import Skill, SkillSource

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataImporter:
    """Import data from JSON files into the database."""
    
    def __init__(self):
        """Initialize the data importer."""
        self.db = SessionLocal()
    
    def __del__(self):
        """Close the database session when done."""
        self.db.close()
    
    def import_heroes(self, file_path: str = "data/heroes.json") -> int:
        """Import heroes from a JSON file.
        
        Args:
            file_path: Path to the heroes JSON file
            
        Returns:
            Number of heroes imported
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                heroes_data = json.load(f)
            
            count = 0
            for hero_data in heroes_data:
                # Check if hero already exists
                existing_hero = self.db.query(Hero).filter(Hero.name == hero_data["name"]).first()
                
                if not existing_hero:
                    hero = Hero(
                        name=hero_data["name"]
                    )
                    self.db.add(hero)
                    count += 1
            
            self.db.commit()
            logger.info(f"Imported {count} new heroes")
            return count
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error importing heroes: {e}")
            return 0
    
    def import_items(self, file_path: str = "data/items.json") -> int:
        """Import items from a JSON file.
        
        Args:
            file_path: Path to the items JSON file
            
        Returns:
            Number of items imported
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                items_data = json.load(f)
            
            count = 0
            for item_data in items_data:
                # Check if item already exists
                existing_item = self.db.query(Item).filter(Item.name == item_data["name"]).first()
                
                if not existing_item:
                    # Map size string to enum
                    size = ItemSize.MEDIUM  # Default
                    size_str = item_data.get("size")
                    if size_str == "small":
                        size = ItemSize.SMALL
                    elif size_str == "medium":
                        size = ItemSize.MEDIUM
                    elif size_str == "large":
                        size = ItemSize.LARGE
                    
                    # Map source string to enum
                    source = ItemSource.UNIVERSAL  # Default
                    source_str = item_data.get("source")
                    if source_str == "hero_specific":
                        source = ItemSource.HERO_SPECIFIC
                    elif source_str == "monster":
                        source = ItemSource.MONSTER
                    
                    item = Item(
                        name=item_data["name"],
                        description=item_data.get("description"),
                        size=size,
                        source=source,
                        hero_id=item_data.get("hero_id"),
                        monster_id=item_data.get("monster_id"),
                        cooldown=item_data.get("cooldown"),
                        effect=item_data.get("effect"),
                        cost=item_data.get("cost")
                    )
                    self.db.add(item)
                    count += 1
            
            self.db.commit()
            logger.info(f"Imported {count} new items")
            return count
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error importing items: {e}")
            return 0
    
    def import_skills(self, file_path: str = "data/skills.json") -> int:
        """Import skills from a JSON file.
        
        Args:
            file_path: Path to the skills JSON file
            
        Returns:
            Number of skills imported
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                skills_data = json.load(f)
            
            count = 0
            for skill_data in skills_data:
                # Check if skill already exists
                existing_skill = self.db.query(Skill).filter(Skill.name == skill_data["name"]).first()
                
                if not existing_skill:
                    # Map source string to enum
                    source = SkillSource.UNIVERSAL  # Default
                    source_str = skill_data.get("source")
                    if source_str == "hero_specific":
                        source = SkillSource.HERO_SPECIFIC
                    elif source_str == "monster":
                        source = SkillSource.MONSTER
                    
                    skill = Skill(
                        name=skill_data["name"],
                        description=skill_data.get("description"),
                        source=source,
                        hero_id=skill_data.get("hero_id"),
                        monster_id=skill_data.get("monster_id"),
                        tier=skill_data.get("tier"),
                        effect=skill_data.get("effect"),
                        types=skill_data.get("types")
                    )
                    self.db.add(skill)
                    count += 1
            
            self.db.commit()
            logger.info(f"Imported {count} new skills")
            return count
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error importing skills: {e}")
            return 0
    
    def run(self, heroes_file: str = "data/heroes.json", items_file: str = "data/items.json", skills_file: str = "data/skills.json") -> bool:
        """Run the complete data import process.
        
        Args:
            heroes_file: Path to the heroes JSON file
            items_file: Path to the items JSON file
            skills_file: Path to the skills JSON file
            
        Returns:
            True if successful, False otherwise
        """
        # Import heroes first to establish relationships
        heroes_count = self.import_heroes(heroes_file)
        logger.info(f"Imported {heroes_count} heroes")
        
        # Import items
        items_count = self.import_items(items_file)
        logger.info(f"Imported {items_count} items")
        
        # Import skills
        skills_count = self.import_skills(skills_file)
        logger.info(f"Imported {skills_count} skills")
        
        return heroes_count >= 0 and items_count >= 0 and skills_count >= 0

def main():
    """Run the data importer."""
    logger.info("Starting data import")
    
    importer = DataImporter()
    success = importer.run()
    
    if success:
        logger.info("Data import completed successfully")
    else:
        logger.error("Data import failed")

if __name__ == "__main__":
    main()