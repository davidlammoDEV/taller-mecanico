from decimal import Decimal
from sqlalchemy import (ForeignKey,Integer, Numeric, String)
from sqlalchemy.orm import (Mapped, mapped_column, relationship)
from models.base import Base


class OrdenDetalleRepuesto(Base):
    __tablename__ = "orden_detalle_repuesto"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    orden_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orden_servicio.id", ondelete="CASCADE"), nullable=False
    )
    repuesto_codigo: Mapped[str] = mapped_column(
        String(20), ForeignKey("repuesto.codigo", ondelete="RESTRICT"), nullable=False
    )
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    precio_aplicado: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    orden = relationship("Orden", back_populates="repuestos")
    repuesto = relationship("Repuesto", back_populates="detalles")

    def __repr__(self) -> str:
        return f"<OrdenDetalleRepuesto orden={self.orden_id} repuesto={self.repuesto_codigo!r}>"