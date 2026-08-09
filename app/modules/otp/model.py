from datetime import datetime

from sqlalchemy import DateTime, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class OTP(Base):
    __tablename__ = "otps"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True
    )

    otp_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    expire_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )