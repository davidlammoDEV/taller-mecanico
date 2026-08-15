from database.connection import SessionLocal
from schemas.vehiculo_schema import VehiculoEntrada, VehiculoSalida, VehiculoUpdate
from services import vehiculo_service
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from models.usuario_model import Usuario
from tokensitos.auth_dependencias import VerificarRoles, require_supervisor

vehiculo_router = APIRouter(
    prefix="/vehiculo",
    tags=["Vehiculo"],
    dependencies=[Depends(require_supervisor)]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@vehiculo_router.get("/{placa}", response_model=VehiculoSalida)
def obtener_vehiculo(placa: str, db:Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return vehiculo_service.obtener_vehiculo(placa, db)

@vehiculo_router.get("/", response_model=List[VehiculoSalida], status_code=status.HTTP_200_OK)
def listar_vehiculos(db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return vehiculo_service.listar_vehiculos(db)

@vehiculo_router.post("/", response_model=VehiculoEntrada, status_code=status.HTTP_200_OK)
def crear_vehiculo(vehiculo: VehiculoEntrada, db:Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return vehiculo_service.crear_vehiculo(vehiculo, db)

@vehiculo_router.put("/{placa}", response_model=VehiculoSalida)
def actualizar_vehiculo_completo(placa: str, carro_update: VehiculoEntrada, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return vehiculo_service.actualizar_vehiculo_completo(placa, carro_update, db)

@vehiculo_router.patch("/{placa}", response_model=VehiculoSalida)
def actualizar_vehiculo_parcial(placa: str, carro_update: VehiculoUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return vehiculo_service.actualizar_vehiculo_parcial(placa, carro_update, db)

@vehiculo_router.delete("/{placa}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_vehiculo_logico(placa: str, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return vehiculo_service.eliminar_vehiculo_logico(placa, db)
