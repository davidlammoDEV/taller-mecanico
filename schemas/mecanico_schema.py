from pydantic import BaseModel
from typing import Optional
from datetime import date

class MecanicoSalida(BaseModel):
    id : int
    documento : str
    nombre : str
    especialidad: Optional[str] | None = None
    telefono : Optional[str] | None = None
    fecha_ingreso : date

class MecanicoEntrada(BaseModel):
    documento : str
    nombre : str
    especialidad: Optional[str] | None = None
    telefono : Optional[str] | None = None
    fecha_ingreso : date

class MecanicoUpdate(BaseModel):
    documento : Optional[str] | None = None
    nombre : Optional[str] | None = None
    especialidad: Optional[str] | None = None
    telefono : Optional[str] | None = None
    fecha_ingreso : Optional[date] | None = None