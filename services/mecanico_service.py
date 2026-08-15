from models.mecanico_model import Mecanico
from schemas.mecanico_schema import MecanicoEntrada, MecanicoUpdate
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

def obtener_mecanico(id:int, db:Session):
    mecanico = db.query(Mecanico).filter(Mecanico.id == id, Mecanico.activo == True).first()
    if mecanico is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mecanico no Encontrado")
    return mecanico

def listar_mecanicos(db: Session):
    return db.query(Mecanico).filter(Mecanico.activo == True).all()


def crear_mecanico(mecanico: MecanicoEntrada, db:Session):
    try:
        mecanico= Mecanico(documento= mecanico.documento,
                        nombre = mecanico.nombre,
                        especialidad = mecanico.especialidad,
                        telefono = mecanico.telefono,
                        fecha_ingreso = mecanico.fecha_ingreso)
        db.add(mecanico)
        db.commit()
        db.refresh(mecanico)
        return mecanico

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El mecánico con documento {mecanico.documento} ya se encuentra registrado")
    except DataError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uno o más campos superan la longitud máxima de caracteres permitida")

def actualizar_mecanico_completo(id: int, cliente_update: MecanicoEntrada, db: Session):
    db_mecanico = db.query(Mecanico).filter(Mecanico.id == id).first()
    if not db_mecanico:
        raise HTTPException(status_code=404, detail="Mecanico no encontrado")

    try:
        for key, value in cliente_update.model_dump().items():
            setattr(db_mecanico, key, value)

        db.commit()
        db.refresh(db_mecanico)
        return db_mecanico

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El mecánico ya se encuentra registrado")
    except DataError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uno o más campos superan la longitud máxima de caracteres permitida")


def actualizar_mecanico_parcial(id: int, mecanico_updata: MecanicoUpdate, db: Session):
    db_mecanico = db.query(Mecanico).filter(Mecanico.id == id, Mecanico.activo == True).first()

    if not db_mecanico:
        raise HTTPException(status_code=404, detail="Mecanico no encontrado o inactivo")
    update_data = mecanico_updata.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")

    try:
        for key, value in update_data.items():
            setattr(db_mecanico, key, value)

        db.commit()
        db.refresh(db_mecanico)
        return db_mecanico

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El mecánico ya se encuentra registrado")
    except DataError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uno o más campos superan la longitud máxima de caracteres permitida")


def eliminar_mecanico_logico(id: int, db: Session):
    db_mecanico = db.query(Mecanico).filter(Mecanico.id == id, Mecanico.activo==True).first()
    if not db_mecanico:
        raise HTTPException(status_code=404, detail="Mecanico no encontrado")
    db_mecanico.activo = False
    db.commit()
    return None

