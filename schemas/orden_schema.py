from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class EstadoOrdenEnum(str, Enum):
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En Proceso"
    COMPLETADO = "Completado"
    CANCELADO = "Cancelado"

class OrdenSalida(BaseModel):
    id : int
    fecha : datetime
    diagnostico : str
    estado: EstadoOrdenEnum
    observaciones : str
    costo_estimado: Decimal
    cliente_id: int
    placa : str
    mecanico_id: int

class OrdenEntrada(BaseModel):
    fecha : date
    diagnostico : str
    estado: EstadoOrdenEnum
    observaciones : str
    costo_estimado: Decimal
    cliente_id: int
    placa : str
    mecanico_id: int

class OrdenActualizar(BaseModel):
    diagnostico: Optional[str] = None
    estado: Optional[EstadoOrdenEnum] = None
    observaciones: Optional[str] = None
    costo_estimado: Optional[Decimal] = None
    mecanico_id: Optional[int] = None