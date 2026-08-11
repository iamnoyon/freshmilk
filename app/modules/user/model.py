from datetime import datetime
from enum import Enum

from sqlalchemy import ARRAY, String, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class AreaEnum(str, Enum):
    MIRPURDOSH = "mirpurdosh"


class ROLE(str, Enum):
    CUSTOMER = "customer"
    DELIVERYMAN = "deliveryman"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    nid: Mapped[str] = mapped_column(nullable=False)
    nid_verified: Mapped[bool] = mapped_column(nullable=False, default=False)

    phone: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    role: Mapped[ROLE] = mapped_column(
        SAEnum(ROLE),
        nullable=False,
        default=ROLE.CUSTOMER
    )

    area: Mapped[AreaEnum] = mapped_column(
        SAEnum(AreaEnum),
        nullable=False
    )

    road: Mapped[str] = mapped_column(nullable=False)
    house: Mapped[str] = mapped_column(nullable=False)
    flat: Mapped[str] = mapped_column(nullable=False)

    permissions: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list,
    )

    createdAt: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    createdBy: Mapped[str] = mapped_column(
        nullable=True,
        default="system"
    )

    updatedAt: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    updatedBy: Mapped[str] = mapped_column(nullable=True)