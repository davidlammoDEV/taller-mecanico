from database.connection import SessionLocal
from schemas.servicio_schema import ServicioEntrada, ServicioSalida, ServicioUpdata
from services import servicio_service
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from models.usuario_model import Usuario
from tokensitos.auth_dependencias import VerificarRoles, require_supervisor

servicio_router = APIRouter(
    prefix="/servicio",
    tags=["Servicio"],
    dependencies=[Depends(require_supervisor)]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@servicio_router.get("/{id}", response_model=ServicioSalida)
def obtener_servicio(id:int, db:Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return servicio_service.obtener_servicio(id, db)

@servicio_router.get("/", response_model=List[ServicioSalida], status_code=status.HTTP_200_OK)
def listar_servicios(db: Session = Depends(get_db)):
    return servicio_service.listar_servicios(db)

@servicio_router.post("/", response_model=ServicioEntrada, status_code=status.HTTP_200_OK)
def crear_servicio(servicio: ServicioEntrada, db:Session = Depends(get_db)):
    return servicio_service.crear_servicio(servicio, db)

@servicio_router.put("/{id}", response_model=ServicioSalida)
def actualizar_servicio_completo(id: int, cliente_update: ServicioEntrada, db: Session = Depends(get_db)):
    return servicio_service.actualizar_servicio_completo(id, cliente_update, db)

@servicio_router.patch("/{id}", response_model=ServicioSalida)
def actualizar_servicio_parcial(id: int, servicio_update: ServicioUpdata, db: Session = Depends(get_db)):
    return servicio_service.actualizar_servicio_parcial(id, servicio_update, db)

@servicio_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_servicio_logico(id: int, db: Session = Depends(get_db)):
    return servicio_service.eliminar_servicio_logico(id, db)

