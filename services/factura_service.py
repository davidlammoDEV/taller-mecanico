from models.factura_model import Factura
from models.orden_model import Orden
from schemas.factura_schema import FacturaActualizar, FacturaEntrada, MetodoPagoEnum
from schemas.orden_schema import EstadoOrdenEnum
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

def obtener_factura(factura_id: int, db: Session):
    factura = db.query(Factura).filter(
        Factura.id == factura_id,
        Factura.activo == True
    ).first()
    if factura is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")
    return factura

def listar_facturas(db: Session):
    facturas = db.query(Factura).filter(Factura.activo == True).all()
    if not facturas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay facturas registradas")
    return facturas

def obtener_factura_por_orden(orden_id: int, db: Session):
    factura = db.query(Factura).filter(
        Factura.orden_id == orden_id,
        Factura.activo == True
    ).first()
    if factura is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe factura para esta orden")
    return factura

def crear_factura(factura: FacturaEntrada, db: Session):
    # Validar que la orden exista y esté completada
    orden = db.query(Orden).filter(Orden.id == factura.orden_id).first()
    if not orden:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    if orden.estado != EstadoOrdenEnum.COMPLETADO.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Solo se puede facturar una orden con estado '{EstadoOrdenEnum.COMPLETADO.value}'"
        )

    # Validar que la orden no tenga factura activa ya
    ya_facturada = db.query(Factura).filter(
        Factura.orden_id == factura.orden_id,
        Factura.activo == True
    ).first()
    if ya_facturada:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esta orden ya tiene una factura")
    # Validar método de pago
    metodo_str = factura.metodo.value if isinstance(factura.metodo, MetodoPagoEnum) else factura.metodo

    nueva_factura = Factura(
        orden_id=factura.orden_id,
        subtotal=factura.subtotal,
        impuestos=factura.impuestos,
        total=factura.total,
        cobro_final=factura.cobro_final,
        metodo=metodo_str
    )
    db.add(nueva_factura)
    db.commit()
    db.refresh(nueva_factura)
    return nueva_factura

def actualizar_factura_parcial(factura_id: int, factura_update: FacturaActualizar, db: Session):
    db_factura = db.query(Factura).filter(
        Factura.id == factura_id,
        Factura.activo == True
    ).first()
    if not db_factura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")

    update_data = factura_update.model_dump(exclude_unset=True)
    if "metodo" in update_data and isinstance(update_data["metodo"], MetodoPagoEnum):
        update_data["metodo"] = update_data["metodo"].value
    for key, value in update_data.items():
        setattr(db_factura, key, value)

    db.commit()
    db.refresh(db_factura)
    return db_factura

def eliminar_factura_logica(factura_id: int, db: Session):
    db_factura = db.query(Factura).filter(
        Factura.id == factura_id,
        Factura.activo == True
    ).first()
    if not db_factura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")
    db_factura.activo = False
    db.commit()
    return None