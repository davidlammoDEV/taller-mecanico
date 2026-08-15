from typing import Optional, List
from sqlalchemy import (Boolean, Integer, String)
from sqlalchemy.orm import (Mapped, mapped_column, relationship,)
from models.base import Base
#from models.repuesto_model import Repuesto

class Proveedor(Base):
    __tablename__ = "proveedor"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    documento: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    nom_empresa: Mapped[Optional[str]] = mapped_column(String(100))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    correo: Mapped[Optional[str]] = mapped_column(String(100))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    repuestos = relationship("Repuesto", back_populates="proveedor")
    def __repr__(self) -> str:
        return f"<Proveedor id={self.id} nombre={self.nombre!r}>"