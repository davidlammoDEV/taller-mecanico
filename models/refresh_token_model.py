from datetime import date
from typing import Optional
from sqlalchemy import (Boolean, Date, ForeignKey,Integer, String, DateTime)
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column, relationship,)
from models.base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    user_log: Mapped[int] = mapped_column(Integer, ForeignKey("user_log.idsuer_log"), nullable=False)
    expira: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self):
        return f"<RefreshToken usuario={self.usuario_id}>"
    