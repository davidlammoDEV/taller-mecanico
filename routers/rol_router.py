from database.connection import SessionLocal
from schemas.rol_schema import *
from services import rol_service
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from models.usuario_model import Usuario
from tokensitos.auth_dependencias import VerificarRoles

rol_router = APIRouter(
    prefix="/Rol",
    tags=["Rol"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@rol_router.get("/", response_model=List[RolSalida], status_code=status.HTTP_200_OK)
def listar_roles(db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([2]))):
    return rol_service.listar_rol(db)

@rol_router.post("/", response_model=RolEntrada, status_code=status.HTTP_200_OK)
def crear_roles(rol: RolEntrada, db:Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([2]))):
    return rol_service.crear_roles(rol, db)

@rol_router.patch("/{idrol}", response_model=RolSalida)
def actualizar_rol_parcial(idrol: int, rol_up: RolUpdata, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([2]))):
    return rol_service.actualizar_roles_parcial(idrol, rol_up, db)

@rol_router.delete("/{idrol}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_rol_logico(idrol: int, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([2]))):
    return rol_service.eliminar_rol_logico(idrol, db)
