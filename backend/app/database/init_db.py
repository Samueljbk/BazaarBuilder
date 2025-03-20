# app/database/init_db.py

import logging
from sqlalchemy import inspect
from app.database.database import engine, Base
from app.models.hero import Hero
from app.models.item import Item
from app.models.skill import Skill
from app.models.monster import Monster
from app.models.enchantment import Enchantment
from app.models.merchant import Merchant

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_db():
    """Initialize the database by creating all tables."""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    # Check if tables already exist
    if existing_tables:
        logger.info(f"Found existing tables: {existing_tables}")
        logger.info("Database already initialized. Skipping.")
    else:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

def reset_db():
    """Reset the database by dropping and recreating all tables."""
    logger.warning("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database reset completed successfully")

if __name__ == "__main__":
    # Use init_db() to initialize the database
    # init_db()
    
    # Use reset_db() to reset the database (CAUTION: this will delete all data)
    reset_db()