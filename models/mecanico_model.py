from datetime import date
from typing import Optional, List
from sqlalchemy import (Boolean, Date, Integer, String, func)
from sqlalchemy.orm import (Mapped, mapped_column, relationship,)
from models.base import Base
#from models import OrdenServicio

class Mecanico(Base):
    __tablename__ = "mecanico"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    documento: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    especialidad: Mapped[Optional[str]] = mapped_column(String(100))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    fecha_ingreso: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.current_date())
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    ordenes: Mapped[List["Orden"]] = relationship(back_populates="mecanico")

    def __repr__(self) -> str:
        return f"<Mecanico id={self.id} nombre={self.nombre!r}>"