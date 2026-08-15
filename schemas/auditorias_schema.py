from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Any, Dict
from datetime import datetime


class AuditoriaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tabla: str
    operacion: str
    registro_id: str
    datos_antes: Optional[Dict[str, Any]] = None
    datos_despues: Optional[Dict[str, Any]] = None
    usuario_db: Optional[str] = None
    fecha_evento: Optional[datetime] = None
    revisado: Optional[bool] = False
    nota_supervisor: Optional[str] = None
    revisado_por: Optional[int] = None
    fecha_revision: Optional[datetime] = None


class AuditoriaRevisionUpdate(BaseModel):
    """Lo que el supervisor envía para marcar/anotar una revisión."""
    revisado: bool = True
    nota_supervisor: Optional[str] = Field(None, max_length=2000)


class CorregirDatoPayload(BaseModel):
    """
    Payload genérico para corregir el dato ACTUAL de la tabla afectada
    por un registro de auditoría. 'cambios' es un dict campo -> nuevo valor,
    validado contra las columnas reales del modelo en el service
    (solo se aceptan campos permitidos, nunca la PK).
    """
    cambios: Dict[str, Any]
    motivo: Optional[str] = Field(None, max_length=500)