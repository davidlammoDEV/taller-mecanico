from models.supervisor_model import Supervisor  
from schemas.supervisor_schema import SupervisorEntrada, SupervisorUpdate
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

def obtener_supervisor(id:int, db:Session):
    supervisor = db.query(Supervisor).filter(Supervisor.id == id, Supervisor.activo == True).first()
    if supervisor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supervisor no Encontrado")
    return supervisor

def listar_supervisores(db: Session):
    return db.query(Supervisor).filter(Supervisor.activo == True).all()


def crear_supervisor(supervisor: SupervisorEntrada, db:Session):
    try:
        supervisor= Supervisor(documento= supervisor.documento,
                        nombre = supervisor.nombre,
                        telefono = supervisor.telefono,
                        fecha_ingreso = supervisor.fecha_ingreso)
        db.add(supervisor)
        db.commit()
        db.refresh(supervisor)
        return supervisor

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El supervisor con documento {supervisor.documento} ya se encuentra registrado")
    except DataError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uno o más campos superan la longitud máxima de caracteres permitida")

def actualizar_supervisor_completo(id: int, supervisor_update: SupervisorEntrada, db: Session):
    db_supervisor = db.query(Supervisor).filter(Supervisor.id == id).first()
    if not db_supervisor:
        raise HTTPException(status_code=404, detail="Supervisor no encontrado")

    try:
        for key, value in supervisor_update.model_dump().items():
            setattr(db_supervisor, key, value)

        db.commit()
        db.refresh(db_supervisor)
        return db_supervisor

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El supervisor ya se encuentra registrado")
    except DataError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uno o más campos superan la longitud máxima de caracteres permitida")


def actualizar_supervisor_parcial(id: int, supervisor_update: SupervisorUpdate, db: Session):
    db_supervisor = db.query(Supervisor).filter(Supervisor.id == id, Supervisor.activo == True).first()

    if not db_supervisor:
        raise HTTPException(status_code=404, detail="Supervisor no encontrado o inactivo")
    update_data = supervisor_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")

    try:
        for key, value in update_data.items():
            setattr(db_supervisor, key, value)

        db.commit()
        db.refresh(db_supervisor)
        return db_supervisor

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El supervisor ya se encuentra registrado")
    except DataError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uno o más campos superan la longitud máxima de caracteres permitida")


def eliminar_supervisor_logico(id: int, db: Session):
    db_supervisor = db.query(Supervisor).filter(Supervisor.id == id, Supervisor.activo==True).first()
    if not db_supervisor:
        raise HTTPException(status_code=404, detail="Supervisor no encontrado")
    db_supervisor.activo = False
    db.commit()
    return None

