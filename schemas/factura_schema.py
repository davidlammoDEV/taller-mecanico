from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class MetodoPagoEnum(str, Enum):
    EFECTIVO = "Efectivo"
    TARJETA_CREDITO = "Tarjeta de Crédito"
    TARJETA_DEBITO = "Tarjeta de Débito"
    TRANSFERENCIA = "Transferencia"

class FacturaEntrada(BaseModel):
    orden_id: int
    subtotal: Decimal
    impuestos: Decimal = Decimal("0")
    total: Decimal
    cobro_final: Decimal
    metodo: MetodoPagoEnum

class FacturaActualizar(BaseModel):
    subtotal: Optional[Decimal] = None
    impuestos: Optional[Decimal] = None
    total: Optional[Decimal] = None
    cobro_final: Optional[Decimal] = None
    metodo: Optional[MetodoPagoEnum] = None

class FacturaSalida(BaseModel):
    id: int
    orden_id: int
    fecha: datetime
    subtotal: Decimal
    impuestos: Decimal
    total: Decimal
    cobro_final: Decimal
    metodo: MetodoPagoEnum