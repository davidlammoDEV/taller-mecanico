from typing import Optional, List, Any
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from tokensitos.auth_dependencias import get_current_user  # AJUSTA a tu módulo real de JWT
from schemas.auditorias_schema import AuditoriaOut, AuditoriaRevisionUpdate, CorregirDatoPayload
from services import auditoria_service

#DAVID POR EL AMOR A DIOS HAGA BIEN LAS IMPORTACIONES

def require_supervisor(current_user=Depends(get_current_user)):
    """Ajusta 'rol'/'role' al nombre real del atributo en tu modelo de usuario."""
    rol = getattr(current_user, "rol", None) or getattr(current_user, "role", None)
    if rol != "supervisor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo un usuario con rol 'supervisor' puede acceder a este recurso",
        )
    return current_user


router = APIRouter(
    prefix="/auditoria",
    tags=["Auditoría"],
    dependencies=[Depends(require_supervisor)],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[AuditoriaOut])
def listar_auditoria(
    skip: int = 0,
    limit: int = 100,
    tabla: Optional[str] = Query(None, description="cliente, vehiculo, proveedor, orden_servicio, factura"),
    operacion: Optional[str] = Query(None, description="INSERT, UPDATE, DELETE, CORRECCION_MANUAL"),
    registro_id: Optional[str] = None,
    revisado: Optional[bool] = None,
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    """Lista los eventos de auditoría, con filtros opcionales. Solo supervisores."""
    return auditoria_service.listar_auditoria(
        db, skip, limit, tabla, operacion, registro_id, revisado, fecha_desde, fecha_hasta
    )


@router.get("/{auditoria_id}", response_model=AuditoriaOut)
def obtener_auditoria(auditoria_id: int, db: Session = Depends(get_db)):
    """Detalle de un evento de auditoría específico."""
    return auditoria_service.obtener_auditoria(db, auditoria_id)


@router.patch("/{auditoria_id}/revision", response_model=AuditoriaOut)
def revisar_auditoria(
    auditoria_id: int,
    data: AuditoriaRevisionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """
    El supervisor marca un evento como revisado y deja una nota.
    No modifica el dato original, solo anota sobre el evento auditado.
    """
    return auditoria_service.marcar_revision(db, auditoria_id, data, current_user)


@router.patch("/{auditoria_id}/corregir-dato")
def corregir_dato_original(
    auditoria_id: int,
    data: CorregirDatoPayload,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
) -> Any:
    """
    El supervisor corrige el dato ACTUAL en la tabla afectada por este
    evento de auditoría. Queda doble rastro: el trigger de PostgreSQL
    audita el UPDATE, y el service agrega un registro 'CORRECCION_MANUAL'
    con el motivo y el supervisor responsable.
    """
    fila_actualizada = auditoria_service.corregir_dato_original(db, auditoria_id, data, current_user)
    return {c.name: getattr(fila_actualizada, c.name) for c in fila_actualizada.__table__.columns}