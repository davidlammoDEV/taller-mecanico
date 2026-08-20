from database.connection import SessionLocal
from schemas.mecanico_schema import MecanicoEntrada, MecanicoSalida, MecanicoUpdate
from services import mecanico_service
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from models.usuario_model import Usuario
from tokensitos.auth_dependencias import VerificarRoles

mecanico_router = APIRouter(
    prefix="/mecanico",
    tags=["Mecanico"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@mecanico_router.get("/{id}", response_model=MecanicoSalida)
def obtener_mecanico(id:int, db:Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([2,3]))):
    return mecanico_service.obtener_mecanico(id, db)

@mecanico_router.get("/", response_model=List[MecanicoSalida], status_code=status.HTTP_200_OK)
def listar_mecanicos(db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([2,3]))):
    return mecanico_service.listar_mecanicos(db)

@mecanico_router.post("/", response_model=MecanicoEntrada, status_code=status.HTTP_200_OK)
def crear_mecanico(mecanico: MecanicoEntrada, db:Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([2,3]))):
    return mecanico_service.crear_mecanico(mecanico, db)

@mecanico_router.put("/{id}", response_model=MecanicoSalida)
def actualizar_mecanico_completo(id: int, cliente_update: MecanicoEntrada, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([2,3]))):
    return mecanico_service.actualizar_mecanico_completo(id, cliente_update, db)

@mecanico_router.patch("/{id}", response_model=MecanicoSalida)
def actualizar_mecanico_parcial(id: int, mecanico_updata: MecanicoUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([2,3]))):
    return mecanico_service.actualizar_mecanico_parcial(id, mecanico_updata, db)

@mecanico_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_mecanico_logico(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([2,3]))):
    return mecanico_service.eliminar_mecanico_logico(id, db)

