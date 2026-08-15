from pydantic import BaseModel, Field
from typing import Optional

class ClienteSalida(BaseModel):
    id : int
    documento : str
    nombre : str
    telefono : Optional[str] | None = None
    correo: Optional[str] | None = None
    direccion : Optional[str] | None = None

class ClienteEntrada(BaseModel):
    documento : str = Field(..., max_length=20, description="Documento de identidad")
    nombre: str = Field(..., max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[str] = Field(None, max_length=100)
    direccion: Optional[str] = Field(None, max_length=200)

class ClienteUpdate(BaseModel):
    documento: Optional[str] = Field(None, max_length=20)
    nombre: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[str] = Field(None, max_length=100)
    direccion: Optional[str] = Field(None, max_length=200)