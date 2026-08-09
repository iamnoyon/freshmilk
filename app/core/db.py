from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

DATABASE_URL="postgresql://postgres:674@localhost:5432/freshmilk"

engine = create_engine(DATABASE_URL)

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = sessionLocal()

    try:
        yield db

    finally:
        db.close()