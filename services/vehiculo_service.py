from models.vehiculo_model import Vehiculo
from schemas.vehiculo_schema import VehiculoEntrada, VehiculoUpdate
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

def obtener_vehiculo(placa: str, db:Session):
    vehiculo= db.query(Vehiculo).filter(Vehiculo.placa == placa, Vehiculo.activo == True).first()
    if vehiculo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehiculo con placa '{placa}' no encontrado")
    return vehiculo

def listar_vehiculos(db: Session):
    vehiculo= db.query(Vehiculo).filter(Vehiculo.activo == True)


    if not vehiculo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lista de vehiculos vacia")
    return vehiculo

def crear_vehiculo(vehiculo: VehiculoEntrada, db:Session):
    vehiculo= Vehiculo(placa= vehiculo.placa,
                     marca= vehiculo.marca,
                     modelo= vehiculo.modelo,
                     ano= vehiculo.ano,
                     color = vehiculo.color,
                     kilometraje = vehiculo.kilometraje,
                     observaciones = vehiculo.observaciones,
                     cliente_id=vehiculo.cliente_id)
    db.add(vehiculo)
    db.commit()
    db.refresh(vehiculo)
    return vehiculo

def actualizar_vehiculo_completo(placa: str, carro_update: VehiculoEntrada, db: Session):
    db_carro = db.query(Vehiculo).filter(Vehiculo.placa == placa).first()
    if not db_carro:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

    for key, value in carro_update.model_dump().items():
        setattr(db_carro, key, value)

    db.commit()
    db.refresh(db_carro)
    return db_carro

def actualizar_vehiculo_parcial(placa: str, carro_update: VehiculoUpdate, db: Session):
    db_carro = db.query(Vehiculo).filter(Vehiculo.placa == placa, Vehiculo.activo == True).first()

    if not db_carro:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado o inactivo")
    update_data = carro_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")

    for key, value in update_data.items():
        setattr(db_carro, key, value)

    db.commit()
    db.refresh(db_carro)
    return db_carro

def eliminar_vehiculo_logico(placa: str, db: Session):
    db_carro = db.query(Vehiculo).filter(Vehiculo.placa == placa, Vehiculo.activo== True).first()
    if not db_carro:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    db_carro.activo = False
    db.commit()
    return None