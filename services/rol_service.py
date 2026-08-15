from models.rol_model import Rol
from schemas.rol_schema import *
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

def listar_rol(db: Session):
    rol = db.query(Rol).filter(Rol.activo == True).all()
    if len(rol) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lista de roles vacia")
    return rol

def crear_roles(rol: RolEntrada, db:Session):
    rol= Rol(nombre= rol.nombre,
                     descripcion = rol.descripcion
    )
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol

def actualizar_roles_parcial(idrol: int, rol_update: RolUpdata, db: Session):
    db_rol = db.query(Rol).filter(Rol.idrol == idrol, Rol.activo == True).first()
    if not db_rol:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_data = rol_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_rol, key, value)

    db.commit()
    db.refresh(db_rol)
    return db_rol

def eliminar_rol_logico(idrol: int, db: Session):
    db_rol = db.query(Rol).filter(Rol.idrol == idrol, Rol.activo==True).first()
    if not db_rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db_rol.activo = False
    db.commit()
    return None
