from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class ClienteSalida(BaseModel):
    id : int
    documento : str
    nombre : str
    telefono : Optional[str] | None = None
    correo: Optional[str] | None = None
    direccion : Optional[str] | None = None

class ClienteEntrada(BaseModel):
    documento : str
    nombre : str
    telefono : Optional[str] | None = None
    correo: Optional[str] | None = None
    direccion : Optional[str] | None = None

class ClienteUpdate(BaseModel):
    documento: Optional[str] = None
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    direccion: Optional[str] = None

class VehiculoSalida(BaseModel):
    placa : str
    marca : str
    modelo : str
    ano : int
    color: str
    kilometraje : int
    observaciones: Optional[str] = None
    cliente_id: int

class VehiculoEntrada(BaseModel):
    placa : str
    marca : str
    modelo : str
    ano : int
    color: str
    kilometraje : int
    observaciones: Optional[str] = None
    cliente_id: int

class VehiculoUpdate(BaseModel):
    placa : Optional[str] = None
    marca : Optional[str] = None
    modelo : Optional[str] = None
    ano : Optional[int] = None
    color: Optional[str] = None
    kilometraje : Optional[int] = None
    observaciones: Optional[str] = None
    cliente_id: Optional[int] = None

class MecanicoSalida(BaseModel):
    id : int
    documento : str
    nombre : str
    especialidad: Optional[str] | None = None
    telefono : Optional[str] | None = None
    fecha_ingreso : date
    estado : bool

class MecanicoEntrada(BaseModel):
    documento : str
    nombre : str
    especialidad: Optional[str] | None = None
    telefono : Optional[str] | None = None
    fecha_ingreso : date
    estado : bool

class MecanicoUpdate(BaseModel):
    documento : Optional[str] | None = None
    nombre : Optional[str] | None = None
    especialidad: Optional[str] | None = None
    telefono : Optional[str] | None = None
    fecha_ingreso : Optional[date] | None = None
    estado : Optional[bool] | None = None

class ServicioSalida(BaseModel):
    id : int
    nombre : str
    costo_base : Decimal
    descripcion : str

class ServicioEntrada(BaseModel):
    nombre : str
    costo_base : Decimal
    descripcion : str

class ServicioUpdata(BaseModel):
    nombre : Optional[str] | None = None
    costo_base : Optional[Decimal] | None = None
    descripcion : Optional[str] | None = None

class ProveedorSalida(BaseModel):
    id : int
    documento : str
    nombre : str
    nom_empresa : str
    telefono: str
    correo : str

class ProveedorEntrada(BaseModel):
    documento : str
    nombre : str
    nom_empresa : str
    telefono: str
    correo : str

class ProveedorUpdata(BaseModel):
    documento : Optional[str] | None = None
    nombre : Optional[str] | None = None
    nom_empresa : Optional[str] | None = None
    telefono: Optional[str] | None = None
    correo : Optional[str] | None = None

class RepuestoSalida(BaseModel):
    codigo : str
    nombre : str
    marca : str
    stock: int
    costo : Decimal
    precio: Decimal
    descripcion : str
    proveedor_id : int

class RepuestoEntrada(BaseModel):
    codigo : str
    nombre : str
    marca : str
    stock: int
    costo : Decimal
    precio: Decimal
    descripcion : str
    proveedor_id : int

class RepuestoUpdata(BaseModel):
    codigo : Optional[str] | None = None
    nombre : Optional[str] | None = None
    marca : Optional[str] | None = None
    stock: Optional[int] | None = None
    costo : Optional[Decimal] | None = None
    precio: Optional[Decimal] | None = None
    descripcion : Optional[str] | None = None
    proveedor_id : Optional[int] | None = None

class OrdenServicioSalida(BaseModel):
    id : int
    fecha : datetime
    diagnostico : str
    estado: str
    observaciones : str
    costo_estimado: Decimal
    cliente_id: int
    placa : str
    mecanico_id: int

class OrdenServicioEntrada(BaseModel):
    fecha : date
    diagnostico : str
    estado: str
    observaciones : str
    costo_estimado: Decimal
    cliente_id: int
    placa : str
    mecanico_id: int

class OrdenServicioActualizar(BaseModel):
    diagnostico: Optional[str] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None
    costo_estimado: Optional[Decimal] = None
    mecanico_id: Optional[int] = None

class FacturaEntrada(BaseModel):
    orden_id: int
    subtotal: Decimal
    impuestos: Decimal = Decimal("0")
    total: Decimal
    cobro_final: Decimal
    metodo: str

class FacturaActualizar(BaseModel):
    subtotal: Optional[Decimal] = None
    impuestos: Optional[Decimal] = None
    total: Optional[Decimal] = None
    cobro_final: Optional[Decimal] = None
    metodo: Optional[str] = None

class FacturaSalida(BaseModel):
    id: int
    orden_id: int
    fecha: datetime
    subtotal: Decimal
    impuestos: Decimal
    total: Decimal
    cobro_final: Decimal
    metodo: str

    model_config = {"from_attributes": True}
