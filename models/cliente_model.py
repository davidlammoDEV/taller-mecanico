from typing import Optional, List
from sqlalchemy import (Boolean, Integer, String)
from sqlalchemy.orm import (Mapped, mapped_column, relationship,)
from models.base import Base

class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    documento: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    correo: Mapped[Optional[str]] = mapped_column(String(100))
    direccion: Mapped[Optional[str]] = mapped_column(String(200), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    vehiculos = relationship("Vehiculo", back_populates="cliente")
    ordenes = relationship("Orden", back_populates="cliente")

    def __repr__(self) -> str:
        return f"<Cliente id={self.id} nombre={self.nombre!r}>"
