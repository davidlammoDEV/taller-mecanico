from decimal import Decimal
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import (Boolean, Integer, Numeric, String, Text)
from sqlalchemy.orm import ( Mapped, mapped_column, relationship,)
from models.base import Base

class Servicio(Base):
    __tablename__ = "servicio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    costo_base: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    detalles = relationship("OrdenDetalleServicio", back_populates="servicio")

    def __repr__(self) -> str:
        return f"<Servicio id={self.id} nombre={self.nombre!r}>"