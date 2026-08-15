from database.connection import SessionLocal
from schemas.orden_schema import OrdenActualizar, OrdenEntrada, OrdenSalida, EstadoOrdenEnum
from services import orden_service
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from models.usuario_model import Usuario
from tokensitos.auth_dependencias import VerificarRoles, require_supervisor

orden_router = APIRouter(
    prefix="/orden",
    tags=["Orden"],
    dependencies=[Depends(require_supervisor)]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@orden_router.get("/{orden_id}", response_model=OrdenSalida)
def obtener_orden(orden_id: int, db: Session = Depends(get_db),  current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return orden_service.obtener_orden(orden_id, db)

@orden_router.get("/", response_model=List[OrdenSalida], status_code=status.HTTP_200_OK)
def listar_ordenes(db: Session = Depends(get_db),  current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return orden_service.listar_ordenes(db)

@orden_router.get("/estado/{estado}", response_model=List[OrdenSalida], status_code=status.HTTP_200_OK)
def listar_ordenes_por_estado(estado: EstadoOrdenEnum, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return orden_service.listar_ordenes_por_estado(estado, db)

@orden_router.post("/", response_model=OrdenSalida, status_code=status.HTTP_201_CREATED)
def crear_orden(orden: OrdenEntrada, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return orden_service.crear_orden(orden, db)

@orden_router.put("/{orden_id}", response_model=OrdenSalida)
def actualizar_orden_completa(orden_id: int, orden_update: OrdenEntrada, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return orden_service.actualizar_orden_completa(orden_id, orden_update, db)

@orden_router.patch("/{orden_id}", response_model=OrdenSalida)
def actualizar_orden_parcial(orden_id: int, orden_update: OrdenActualizar, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return orden_service.actualizar_orden_parcial(orden_id, orden_update, db)

@orden_router.delete("/{orden_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_orden_logica(orden_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return orden_service.eliminar_orden_logica(orden_id, db)