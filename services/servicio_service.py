from models.servicio_model import Servicio
from schemas.servicio_schema import ServicioEntrada, ServicioUpdata
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

def obtener_servicio(id:int, db:Session):
    servicio = db.query(Servicio).filter(Servicio.id == id, Servicio.activo == True).first()
    if servicio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no Encontrado")
    return servicio

def listar_servicios(db: Session):
    servicio = db.query(Servicio).filter(Servicio.activo == True).all()
    if len(servicio) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lista de servicios vacia")
    return servicio

def crear_servicio(servicio: ServicioEntrada, db:Session):
    servicio= Servicio(nombre= servicio.nombre,
                     costo_base = servicio.costo_base,
                     descripcion = servicio.descripcion)
    db.add(servicio)
    db.commit()
    db.refresh(servicio)
    return servicio

def actualizar_servicio_completo(id: int, cliente_update: ServicioEntrada, db: Session):
    db_servicio = db.query(Servicio).filter(Servicio.id == id).first()
    if not db_servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    for key, value in cliente_update.model_dump().items():
        setattr(db_servicio, key, value)

    db.commit()
    db.refresh(db_servicio)
    return db_servicio

def actualizar_servicio_parcial(id: int, servicio_update: ServicioUpdata, db: Session):
    db_servicio = db.query(Servicio).filter(Servicio.id == id, Servicio.activo == True).first()
    if not db_servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    update_data = servicio_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_servicio, key, value)

    db.commit()
    db.refresh(db_servicio)
    return db_servicio

def eliminar_servicio_logico(id: int, db: Session):
    db_servicio = db.query(Servicio).filter(Servicio.id == id, Servicio.activo==True).first()
    if not db_servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    db_servicio.activo = False
    db.commit()
    return None

