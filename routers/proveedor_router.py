from database.connection import SessionLocal
from schemas.proveedor_schema import ProveedorEntrada, ProveedorSalida, ProveedorUpdata
from services import proveedor_service
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from tokensitos.auth_dependencias import VerificarRoles, require_supervisor
from models.usuario_model import Usuario

proveedor_router = APIRouter(
    prefix="/proveedor",
    tags=["Proveedor"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@proveedor_router.get("/{id}", response_model=ProveedorSalida)
def obtener_proveedor(id:int, db:Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([2,3]))):
    return proveedor_service.obtener_proveedor(id, db)

@proveedor_router.get("/", response_model=List[ProveedorSalida], status_code=status.HTTP_200_OK)
def listar_proveedores(db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([2,3]))):
    return proveedor_service.listar_proveedores(db)

@proveedor_router.post("/", response_model=ProveedorEntrada, status_code=status.HTTP_200_OK)
def crear_proveedor(proveedor: ProveedorEntrada, db:Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([2,3]))):
    return proveedor_service.crear_proveedor(proveedor, db)

@proveedor_router.put("/{id}", response_model=ProveedorSalida)
def actualizar_proveedor_completo(id: int, proveedor_update: ProveedorEntrada, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([2,3]))):
    return proveedor_service.actualizar_proveedor_completo(id, proveedor_update, db)

@proveedor_router.patch("/{id}", response_model=ProveedorSalida)
def actualizar_mecanico_parcial(id: int, proveedor_update: ProveedorUpdata, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([2,3]))):
    return proveedor_service.actualizar_mecanico_parcial(id, proveedor_update, db)

@proveedor_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_proveedor_logico(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([2]))):
    return proveedor_service.eliminar_proveedor_logico(id, db)
