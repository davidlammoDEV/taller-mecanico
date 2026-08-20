from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from sqlalchemy import (Boolean, CheckConstraint, DateTime, ForeignKey,Integer, Numeric, String, Text, func)
from sqlalchemy.orm import (Mapped, mapped_column, relationship)
from models.base import Base

class Orden(Base):
    __tablename__ = "orden_servicio"
    __table_args__ = (
        CheckConstraint(
            "estado IN ('Pendiente', 'En Proceso', 'Completado', 'Cancelado')",
            name="ck_orden_estado",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fecha: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    diagnostico: Mapped[Optional[str]] = mapped_column(Text)
    estado: Mapped[str] = mapped_column(String(30), nullable=False, default="Recibido")
    observaciones: Mapped[Optional[str]] = mapped_column(Text)
    costo_estimado: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    cliente_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cliente.id", ondelete="RESTRICT"), nullable=False
    )
    placa: Mapped[str] = mapped_column(
        String(10), ForeignKey("vehiculo.placa", ondelete="RESTRICT"), nullable=False
    )
    mecanico_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("mecanico.id", ondelete="RESTRICT"), nullable=False
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    
    cliente = relationship("Cliente", back_populates="ordenes")
    vehiculo = relationship("Vehiculo", back_populates="ordenes")
    mecanico = relationship("Mecanico", back_populates="ordenes")
    servicios = relationship("OrdenDetalleServicio", back_populates="orden", cascade="all, delete-orphan")
    repuestos = relationship("OrdenDetalleRepuesto", back_populates="orden",cascade="all, delete-orphan")
    factura = relationship("Factura", back_populates="orden")

    def __repr__(self) -> str:
        return f"<OrdenServicio id={self.id} estado={self.estado!r}>"
