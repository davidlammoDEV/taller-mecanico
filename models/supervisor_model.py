from datetime import date
from typing import Optional, List
from sqlalchemy import (Boolean, Date, Integer, String, func)
from sqlalchemy.orm import (Mapped, mapped_column, relationship,)
from models.base import Base

class Supervisor(Base):
    __tablename__ = "supervisor"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    documento: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    fecha_ingreso: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.current_date())
    activo: Mapped[bool] = mapped_column(Boolean, default=True)


    def __repr__(self) -> str:
        return f"<Mecanico id={self.id} nombre={self.nombre!r}>"
