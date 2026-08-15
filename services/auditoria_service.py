from datetime import datetime
from typing import Optional, Any, Dict

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models.auditorias_model import Auditoria
from models.cliente_model import Cliente
from models.vehiculo_model import Vehiculo
from models.proveedor_model import Proveedor
from models.orden_model import Orden
from models.factura_model import Factura
from schemas.auditorias_schema import AuditoriaRevisionUpdate, CorregirDatoPayload


TABLA_MODELOS = {
    "cliente": (Cliente, "id", int),
    "vehiculo": (Vehiculo, "placa", str),
    "proveedor": (Proveedor, "id", int),
    "orden_servicio": (Orden, "id", int),
    "factura": (Factura, "id", int),
}

CAMPOS_PROHIBIDOS = {"id", "placa"}


def _modelo_a_dict(instancia) -> Dict[str, Any]:
    return {
        c.name: getattr(instancia, c.name)
        for c in instancia.__table__.columns
    }


def _usuario_id(current_user) -> Optional[int]:
    return getattr(current_user, "id", None)


def listar_auditoria(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    tabla: Optional[str] = None,
    operacion: Optional[str] = None,
    registro_id: Optional[str] = None,
    revisado: Optional[bool] = None,
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
):
    query = db.query(Auditoria)

    if tabla:
        query = query.filter(Auditoria.tabla == tabla)
    if operacion:
        query = query.filter(Auditoria.operacion == operacion)
    if registro_id:
        query = query.filter(Auditoria.registro_id == registro_id)
    if revisado is not None:
        query = query.filter(Auditoria.revisado == revisado)
    if fecha_desde:
        query = query.filter(Auditoria.fecha_evento >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Auditoria.fecha_evento <= fecha_hasta)

    return (
        query.order_by(Auditoria.fecha_evento.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def obtener_auditoria(db: Session, auditoria_id: int) -> Auditoria:
    registro = db.query(Auditoria).filter(Auditoria.id == auditoria_id).first()
    if not registro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de auditoría no encontrado")
    return registro

def marcar_revision(
    db: Session,
    auditoria_id: int,
    data: AuditoriaRevisionUpdate,
    current_user,
) -> Auditoria:
    registro = obtener_auditoria(db, auditoria_id)

    registro.revisado = data.revisado
    registro.nota_supervisor = data.nota_supervisor
    registro.revisado_por = _usuario_id(current_user)
    registro.fecha_revision = datetime.utcnow()

    db.commit()
    db.refresh(registro)
    return registro


def corregir_dato_original(
    db: Session,
    auditoria_id: int,
    data: CorregirDatoPayload,
    current_user,
):
    registro_auditoria = obtener_auditoria(db, auditoria_id)

    if registro_auditoria.tabla not in TABLA_MODELOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La tabla '{registro_auditoria.tabla}' no está habilitada para corrección desde auditoría",
        )

    Modelo, columna_pk, tipo_pk = TABLA_MODELOS[registro_auditoria.tabla]

    try:
        valor_pk = tipo_pk(registro_auditoria.registro_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="registro_id inválido para esta tabla")

    fila = db.query(Modelo).filter(getattr(Modelo, columna_pk) == valor_pk).first()
    if not fila:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El registro original ({registro_auditoria.tabla}={valor_pk}) ya no existe",
        )

    columnas_validas = {c.name for c in fila.__table__.columns}
    campos_invalidos = (set(data.cambios.keys()) - columnas_validas) | (set(data.cambios.keys()) & CAMPOS_PROHIBIDOS)
    if campos_invalidos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Campos no permitidos en 'cambios': {sorted(campos_invalidos)}",
        )

    datos_antes = _modelo_a_dict(fila)

    for campo, valor in data.cambios.items():
        setattr(fila, campo, valor)

    try:
        db.flush()  # dispara los triggers de validación/auditoría de PostgreSQL
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig))

    datos_despues = _modelo_a_dict(fila)

    correccion = Auditoria(
        tabla=registro_auditoria.tabla,
        operacion="CORRECCION_MANUAL",
        registro_id=registro_auditoria.registro_id,
        datos_antes=datos_antes,
        datos_despues=datos_despues,
        usuario_db=f"supervisor_id:{_usuario_id(current_user)}",
        fecha_evento=datetime.utcnow(),
        revisado=True,
        nota_supervisor=data.motivo,
        revisado_por=_usuario_id(current_user),
        fecha_revision=datetime.utcnow(),
    )
    db.add(correccion)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig))

    db.refresh(fila)
    return fila