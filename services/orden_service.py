from models.orden_model import Orden
from models.cliente_model import Cliente
from models.vehiculo_model import Vehiculo
from models.mecanico_model import Mecanico
from schemas.orden_schema import OrdenActualizar, OrdenEntrada, EstadoOrdenEnum
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

def obtener_orden(orden_id: int, db: Session):
    orden = db.query(Orden).filter(
        Orden.id == orden_id,
        Orden.activo == True
    ).first()
    if orden is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return orden

def listar_ordenes(db: Session):
    ordenes = db.query(Orden).filter(Orden.activo == True).all()
    if not ordenes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay órdenes registradas")
    return ordenes

def listar_ordenes_por_estado(estado: EstadoOrdenEnum, db: Session):
    ordenes = db.query(Orden).filter(
        Orden.estado == estado.value,
        Orden.activo == True
    ).all()
    if not ordenes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay órdenes con ese estado")
    return ordenes

def crear_orden(orden: OrdenEntrada, db: Session):
    # Validar FK
    if not db.query(Cliente).filter(Cliente.id == orden.cliente_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    if not db.query(Vehiculo).filter(Vehiculo.placa == orden.placa, Vehiculo.activo == True).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehículo no encontrado")
    if not db.query(Mecanico).filter(Mecanico.id == orden.mecanico_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mecánico no encontrado")

    # Crear la orden
    nueva_orden = Orden(
        diagnostico=orden.diagnostico,
        estado=orden.estado.value if isinstance(orden.estado, EstadoOrdenEnum) else orden.estado,
        observaciones=orden.observaciones,
        costo_estimado=orden.costo_estimado,
        cliente_id=orden.cliente_id,
        placa=orden.placa,
        mecanico_id=orden.mecanico_id
    )

    db.add(nueva_orden)
    db.commit()
    db.refresh(nueva_orden)

    return nueva_orden

def actualizar_orden_completa(orden_id: int, orden_update: OrdenEntrada, db: Session):
    db_orden = db.query(Orden).filter(
        Orden.id == orden_id,
        Orden.activo == True
    ).first()
    if not db_orden:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")

    data = orden_update.model_dump(exclude={"servicios", "repuestos"})

    if isinstance(data.get("estado"), EstadoOrdenEnum):
        data["estado"] = data["estado"].value

    for key, value in data.items():
        setattr(db_orden, key, value)

    db.commit()
    db.refresh(db_orden)
    return db_orden

def actualizar_orden_parcial(orden_id: int, orden_update: OrdenActualizar, db: Session):
    db_orden = db.query(Orden).filter(
        Orden.id == orden_id,
        Orden.activo == True
    ).first()
    if not db_orden:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")

    update_data = orden_update.model_dump(exclude_unset=True)
    if "estado" in update_data and isinstance(update_data["estado"], EstadoOrdenEnum):
        update_data["estado"] = update_data["estado"].value

    for key, value in update_data.items():
        setattr(db_orden, key, value)

    db.commit()
    db.refresh(db_orden)
    return db_orden

def eliminar_orden_logica(orden_id: int, db: Session):
    db_orden = db.query(Orden).filter(
        Orden.id == orden_id,
        Orden.activo == True
    ).first()
    if not db_orden:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    if db_orden.estado == EstadoOrdenEnum.COMPLETADO.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar una orden completada")
    db_orden.activo = False
    db.commit()
    return None