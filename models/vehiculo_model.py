from typing import Optional, List
from sqlalchemy import (Boolean, ForeignKey,Integer, String, Text,)
from sqlalchemy.orm import (Mapped, mapped_column, relationship)
from models.base import Base
#from models.cliente_model import Cliente
#from models.ordenServicio_model import OrdenServicio

class Vehiculo(Base):
    __tablename__ = "vehiculo"

    placa: Mapped[str] = mapped_column(String(10), primary_key=True)
    marca: Mapped[str] = mapped_column(String(50), nullable=False)
    modelo: Mapped[str] = mapped_column(String(50), nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    color: Mapped[Optional[str]] = mapped_column(String(30))
    kilometraje: Mapped[int] = mapped_column(Integer, default=0)
    observaciones: Mapped[Optional[str]] = mapped_column(Text)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    cliente_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cliente.id", ondelete="RESTRICT"), nullable=False
    )

    cliente = relationship("Cliente", back_populates="vehiculos")
    ordenes = relationship("Orden", back_populates="vehiculo")

    def __repr__(self) -> str:
        return f"<Vehiculo placa={self.placa!r} marca={self.marca!r}>"