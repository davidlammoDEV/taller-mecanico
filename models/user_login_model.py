from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.usuario_model import Usuario
    from models.rol_model import Rol

class User_Log(Base):
    __tablename__ = "user_log"

    idsuer_log: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    iduser: Mapped[str] = mapped_column(String(30), ForeignKey("usuarios.iduser"), nullable=False)
    idrol: Mapped[int] = mapped_column(Integer, ForeignKey("rol.idrol"), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relaciones
    usuario: Mapped[Usuario] = relationship("Usuario", back_populates="login_data")
    rol: Mapped[Rol] = relationship("Rol")

    def __repr__(self) -> str:
        return f"<User_Log id={self.iduser_log} iduser={self.iduser!r} idrol={self.idrol}>"