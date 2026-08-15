from pydantic import BaseModel
from typing import Optional

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