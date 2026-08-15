from datetime import datetime
from decimal import Decimal
from sqlalchemy import (Boolean, CheckConstraint, DateTime, ForeignKey,Integer, Numeric, String, func,)
from sqlalchemy.orm import (Mapped, mapped_column, relationship)
from models.base import Base


class Factura(Base):
    __tablename__ = "factura"
    __table_args__ = (
        CheckConstraint(
            "metodo IN ('Efectivo', 'Tarjeta de Crédito', 'Tarjeta de Débito', 'Transferencia')",
            name="ck_factura_metodo",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    orden_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orden_servicio.id", ondelete="RESTRICT"), nullable=False, unique=True
    )
    fecha: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    impuestos: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0"))
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    cobro_final: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    metodo: Mapped[str] = mapped_column(String(50), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    orden = relationship("Orden", back_populates="factura")

    def __repr__(self) -> str:
        return f"<Factura id={self.id} total={self.total}>"