from decimal import Decimal
from sqlalchemy import (ForeignKey,Integer, Numeric)
from sqlalchemy.orm import (Mapped, mapped_column, relationship,)
from models.base import Base

class OrdenDetalleServicio(Base):
    __tablename__ = "orden_detalle_servicio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    orden_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orden_servicio.id", ondelete="CASCADE"), nullable=False
    )
    servicio_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("servicio.id", ondelete="RESTRICT"), nullable=False
    )
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    precio_aplicado: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    orden = relationship("Orden", back_populates="servicios")
    servicio = relationship("Servicio", back_populates="detalles")

    def __repr__(self) -> str:
        return f"<OrdenDetalleServicio orden={self.orden_id} servicio={self.servicio_id}>"