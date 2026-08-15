from decimal import Decimal
from typing import Optional, List
from sqlalchemy import (Boolean, ForeignKey,Integer, Numeric, String, Text)
from sqlalchemy.orm import (Mapped, mapped_column, relationship,)
from models.base import Base
#from models.proveedor_model import Proveedor
#from models.ordenDetalleRepuesto_model import OrdenDetalleRepuesto

class Repuesto(Base):
    __tablename__ = "repuesto"

    codigo: Mapped[str] = mapped_column(String(20), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    marca: Mapped[Optional[str]] = mapped_column(String(50))
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    costo: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    precio: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    proveedor_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("proveedor.id", ondelete="SET NULL")
    )

    proveedor = relationship("Proveedor", back_populates="repuestos")
    detalles = relationship("OrdenDetalleRepuesto", back_populates="repuesto")

    def __repr__(self) -> str:
        return f"<Repuesto codigo={self.codigo!r} nombre={self.nombre!r}>"