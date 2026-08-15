from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List 
from sqlalchemy import (BigInteger, CheckConstraint, Date, DateTime, ForeignKey,Integer, Numeric, String, Text, func,)
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column, relationship,)
class Base(DeclarativeBase):
    pass

#  Cliente
 
class Cliente(Base):
    __tablename__ = "cliente"
 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    documento: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    correo: Mapped[Optional[str]] = mapped_column(String(100))
    direccion: Mapped[Optional[str]] = mapped_column(String(200))
 
    # vinculo
    vehiculos: Mapped[List["Vehiculo"]] = relationship(back_populates="cliente")
    ordenes: Mapped[List["OrdenServicio"]] = relationship(back_populates="cliente")
 
    def __repr__(self) -> str:
        return f"<Cliente id={self.id} nombre={self.nombre!r}>"
 
 
# Vehículo

class Vehiculo(Base):
    __tablename__ = "vehiculo"
 
    placa: Mapped[str] = mapped_column(String(10), primary_key=True)
    marca: Mapped[str] = mapped_column(String(50), nullable=False)
    modelo: Mapped[str] = mapped_column(String(50), nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    color: Mapped[Optional[str]] = mapped_column(String(30))
    kilometraje: Mapped[int] = mapped_column(Integer, default=0)
    observaciones: Mapped[Optional[str]] = mapped_column(Text)
    cliente_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cliente.id", ondelete="RESTRICT"), nullable=False
    )
 
    # vinculo
    cliente: Mapped["Cliente"] = relationship(back_populates="vehiculos")
    ordenes: Mapped[List["OrdenServicio"]] = relationship(back_populates="vehiculo")
 
    def __repr__(self) -> str:
        return f"<Vehiculo placa={self.placa!r} marca={self.marca!r}>"
 
 
# Mecánico

class Mecanico(Base):
    __tablename__ = "mecanico"
    __table_args__ = (
        CheckConstraint("estado IN ('Activo', 'Inactivo')", name="ck_mecanico_estado"),
    )
 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    documento: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    especialidad: Mapped[Optional[str]] = mapped_column(String(100))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    fecha_ingreso: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.current_date())
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="Activo")
 
    # vinculos
    ordenes: Mapped[List["OrdenServicio"]] = relationship(back_populates="mecanico")
 
    def __repr__(self) -> str:
        return f"<Mecanico id={self.id} nombre={self.nombre!r}>"
  
#  Servicio
 
class Servicio(Base):
    __tablename__ = "servicio"
 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    costo_base: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
 
    # vinculos
    detalles: Mapped[List["OrdenDetalleServicio"]] = relationship(back_populates="servicio")
    def __repr__(self) -> str:
        return f"<Servicio id={self.id} nombre={self.nombre!r}>"
 
 
# Proveedor
 
class Proveedor(Base):
    __tablename__ = "proveedor"
 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    documento: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    nom_empresa: Mapped[Optional[str]] = mapped_column(String(100))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    correo: Mapped[Optional[str]] = mapped_column(String(100))
 
    # Vinculos
    repuestos: Mapped[List["Repuesto"]] = relationship(back_populates="proveedor")
 
    def __repr__(self) -> str:
        return f"<Proveedor id={self.id} nombre={self.nombre!r}>"
 
 
#  Repuesto
 
class Repuesto(Base):
    __tablename__ = "repuesto"
 
    codigo: Mapped[str] = mapped_column(String(20), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    marca: Mapped[Optional[str]] = mapped_column(String(50))
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    costo: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    precio: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    proveedor_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("proveedor.id", ondelete="SET NULL")
    )
 
    # vinculadores
    proveedor: Mapped[Optional["Proveedor"]] = relationship(back_populates="repuestos")
    detalles: Mapped[List["OrdenDetalleRepuesto"]] = relationship(back_populates="repuesto")
 
    def __repr__(self) -> str:
        return f"<Repuesto codigo={self.codigo!r} nombre={self.nombre!r}>"
 
 
#   Orden de Servicio

class OrdenServicio(Base):
    __tablename__ = "orden_servicio"
    __table_args__ = (
        CheckConstraint(
            "estado IN ('Recibido', 'En Proceso', 'Completado', 'Cancelado')",
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
 
    # Vinculos
    cliente: Mapped["Cliente"] = relationship(back_populates="ordenes")
    vehiculo: Mapped["Vehiculo"] = relationship(back_populates="ordenes")
    mecanico: Mapped["Mecanico"] = relationship(back_populates="ordenes")
    servicios: Mapped[List["OrdenDetalleServicio"]] = relationship(
        back_populates="orden", cascade="all, delete-orphan"
    )
    repuestos: Mapped[List["OrdenDetalleRepuesto"]] = relationship(
        back_populates="orden", cascade="all, delete-orphan"
    )
    factura: Mapped[Optional["Factura"]] = relationship(back_populates="orden")
 
    def __repr__(self) -> str:
        return f"<OrdenServicio id={self.id} estado={self.estado!r}>"
 
 

# Orden (NEXUS) Servicio  
 
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
 
    # Relaciones
    orden: Mapped["OrdenServicio"] = relationship(back_populates="servicios")
    servicio: Mapped["Servicio"] = relationship(back_populates="detalles")
 
    def __repr__(self) -> str:
        return f"<OrdenDetalleServicio orden={self.orden_id} servicio={self.servicio_id}>"
 
 

# Orden ↔ Repuesto  (Conexión NEXUS)
 
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
 
    # Relacion
    orden: Mapped["OrdenServicio"] = relationship(back_populates="repuestos")
    repuesto: Mapped["Repuesto"] = relationship(back_populates="detalles")
 
    def __repr__(self) -> str:
        return f"<OrdenDetalleRepuesto orden={self.orden_id} repuesto={self.repuesto_codigo!r}>"
 
 
#  Factura 
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
 
    # Relaciones
    orden: Mapped["OrdenServicio"] = relationship(back_populates="factura")
 
    def __repr__(self) -> str:
        return f"<Factura id={self.id} total={self.total}>"