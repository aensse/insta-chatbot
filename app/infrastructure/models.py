from enum import StrEnum, auto

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db_config import Base


class ThreadStatus(StrEnum):
    PENDING = auto()
    BLOCKED = auto()


class ThreadInfo(Base):
    __tablename__ = "threads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    instagram_user_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    instagram_thread_id: Mapped[str] = mapped_column(String, unique=True, index=True)

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(Enum(ThreadStatus), nullable=False, default=ThreadStatus.PENDING)

