from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.user_login_model import User_Log

class Usuario(Base):
    __tablename__ = "usuarios"

    iduser: Mapped[str] = mapped_column(String(30), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False)
    apellido: Mapped[str] = mapped_column(String(30), nullable=False)
    correo: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    contrase: Mapped[str] = mapped_column(String(100), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    login_data: Mapped[Optional[User_Log]] = relationship("User_Log", back_populates="usuario", uselist=False)

    def __repr__(self) -> str:
        return f"<Usuario iduser={self.iduser!r} correo={self.correo!r}>"