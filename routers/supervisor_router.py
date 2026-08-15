from database.connection import SessionLocal
from schemas.supervisor_schema import SupervisorEntrada, SupervisorSalida, SupervisorUpdate
from services import supervisor_service
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from tokensitos.auth_dependencias import require_cliente, require_mecanico, require_supervisor

supervisor_router = APIRouter(
    prefix="/supervisor",
    tags=["Supervisor"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@supervisor_router.get("/{id}", response_model=SupervisorSalida)
def obtener_supervisor(id:int, db:Session = Depends(get_db), current_user = Depends(require_cliente)):
    return supervisor_service.obtener_supervisor(id, db)

@supervisor_router.get("/", response_model=List[SupervisorSalida], status_code=status.HTTP_200_OK)
def listar_supervisores(db: Session = Depends(get_db), current_user = Depends(require_cliente)):
    return supervisor_service.listar_supervisores(db)

@supervisor_router.post("/", response_model=SupervisorEntrada, status_code=status.HTTP_200_OK)
def crear_supervisor(supervisor: SupervisorEntrada, db:Session = Depends(get_db), current_user = Depends(require_supervisor)):
    return supervisor_service.crear_supervisor(supervisor, db)

@supervisor_router.put("/{id}", response_model=SupervisorSalida)
def actualizar_supervisor_completo(id: int, supervisor_update: SupervisorEntrada, db: Session = Depends(get_db), current_user = Depends(require_supervisor)):
    return supervisor_service.actualizar_supervisor_completo(id, supervisor_update, db)

@supervisor_router.patch("/{id}", response_model=SupervisorSalida)
def actualizar_supervisor_parcial(id: int, supervisor_update: SupervisorUpdate, db: Session = Depends(get_db), current_user = Depends(require_supervisor)):
    return supervisor_service.actualizar_supervisor_parcial(id, supervisor_update, db)

@supervisor_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_supervisor_logico(id: int, db: Session = Depends(get_db), current_user = Depends(require_supervisor)):
    return supervisor_service.eliminar_supervisor_logico(id, db)

