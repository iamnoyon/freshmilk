from fastapi import FastAPI
from app.core.db import Base, engine
from app.core.seed import seed_superadmin
from .register_routes import router as api_router


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def on_startup():
    seed_superadmin()

app.include_router(api_router)