from database.connection import SessionLocal
from schemas.repuesto_schema import RepuestoEntrada, RepuestoSalida, RepuestoUpdata
from services import repuesto_service
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from models.usuario_model import Usuario
from tokensitos.auth_dependencias import VerificarRoles

repuesto_router = APIRouter(
    prefix="/repuesto",
    tags=["Repuesto"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@repuesto_router.get("/{codigo}", response_model=RepuestoSalida)
def obtener_repuesto(codigo:str, db:Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return repuesto_service.obtener_repuesto(codigo, db)

@repuesto_router.get("/", response_model=List[RepuestoSalida], status_code=status.HTTP_200_OK)
def listar_repuestos(db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return repuesto_service.listar_repuestos(db)

@repuesto_router.post("/", response_model=RepuestoSalida, status_code=status.HTTP_200_OK)
def crear_repuestos(repuesto: RepuestoEntrada, db:Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return repuesto_service.crear_repuesto(repuesto, db)

@repuesto_router.put("/{codigo}", response_model=RepuestoSalida)
def actualizar_repuesto_completo(codigo: str, proveedor_update: RepuestoEntrada, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return repuesto_service.actualizar_repuesto_completo(codigo, proveedor_update, db)

@repuesto_router.patch("/{codigo}", response_model=RepuestoSalida)
def actualizar_repuesto_parcial(codigo: str, repuesto_updata: RepuestoUpdata, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return repuesto_service.actualizar_repuesto_parcial(codigo, repuesto_updata, db)

@repuesto_router.delete("/{codigo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_repuesto_logico(codigo: str, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return repuesto_service.eliminar_repuesto_logico(codigo, db)