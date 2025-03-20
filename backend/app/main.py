from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import hero_routes, item_routes, skill_routes, build_routes, inventory_routes
from .database.database import engine
from .models import hero, item, skill, build

# Create database tables
hero.Base.metadata.create_all(bind=engine)
item.Base.metadata.create_all(bind=engine)
skill.Base.metadata.create_all(bind=engine)
build.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="The Bazaar Game Assistant API",
    description="API for The Bazaar Game Assistant web app",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(hero_routes.router)
app.include_router(item_routes.router)
app.include_router(skill_routes.router)
app.include_router(build_routes.router)
app.include_router(inventory_routes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to The Bazaar Game Assistant API"}