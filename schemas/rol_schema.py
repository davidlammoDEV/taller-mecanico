from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class RolSalida(BaseModel):
    nombre : str
    descripcion : str

class RolEntrada(BaseModel):
    nombre : str
    descripcion : str


class RolUpdata(BaseModel):
    nombre : Optional[str] | None = None
    descripcion : Optional[str] | None = None