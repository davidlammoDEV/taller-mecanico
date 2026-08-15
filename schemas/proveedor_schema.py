from pydantic import BaseModel
from typing import Optional

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