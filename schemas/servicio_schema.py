from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

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