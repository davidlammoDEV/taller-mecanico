from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

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