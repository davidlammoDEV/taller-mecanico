from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class User_Salida(BaseModel):
    iduser : str
    nombre : str
    apellido : str
    correo : str
    contrase: str


class User_Entrada(BaseModel):
    iduser : str
    nombre : str
    apellido : str
    correo : str
    contrase: str

class User_Updata(BaseModel):
    iduser : Optional[str] | None = None
    nombre : Optional[str] | None = None
    apellido : Optional[str] | None = None
    correo : Optional[str] | None = None
    contrase: Optional[str] | None = None