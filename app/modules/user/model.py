from enum import Enum
from app.core.db import Base
from sqlalchemy.orm import mapped_column, Mapped


class AreaEnum(str, Enum):
    MIRPURDOSH = 'mirpurdosh'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(index=True, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    nid: Mapped[str] = mapped_column(nullable=False)
    nid_verified: Mapped[bool] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    area: Mapped[AreaEnum] = mapped_column(nullable=False)
    road: Mapped[str] = mapped_column(nullable=False)
    house: Mapped[str] = mapped_column(nullable=False)
    flat: Mapped[str] = mapped_column(nullable=False)
