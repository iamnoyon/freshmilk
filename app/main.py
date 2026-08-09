from fastapi import FastAPI
from app.core.db import Base, engine
from .register_routes import router as api_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(api_router)