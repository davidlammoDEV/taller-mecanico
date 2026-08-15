from database.connection import SessionLocal
from schemas.cliente_schema import ClienteEntrada, ClienteSalida, ClienteUpdate
from services import cliente_service
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from models.usuario_model import Usuario
from tokensitos.auth_dependencias import require_cliente, require_mecanico, require_supervisor

cliente_router = APIRouter(
    prefix="/cliente",
    tags=["Cliente"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@cliente_router.get("/{id}", response_model=ClienteSalida)
def obtener_cliente(id:int, db:Session = Depends(get_db), current_user: Usuario = Depends(require_cliente)):
    return cliente_service.obtener_cliente(id, db)

@cliente_router.get("/", response_model=List[ClienteSalida], status_code=status.HTTP_200_OK)
def listar_clientes(db: Session = Depends(get_db), current_user: Usuario = Depends(require_cliente)):
    return cliente_service.listar_clientes(db)

@cliente_router.post("/", response_model=ClienteEntrada, status_code=status.HTTP_200_OK)
def crear_cliente(cliente: ClienteEntrada, db:Session = Depends(get_db), current_user: Usuario = Depends(require_mecanico)):
    return cliente_service.crear_cliente(cliente, db)

@cliente_router.put("/{id}", response_model=ClienteSalida)
def actualizar_cliente_completo(id: int, cliente_update: ClienteEntrada, db: Session = Depends(get_db), current_user: Usuario = Depends(require_mecanico)):
    return cliente_service.actualizar_cliente_completo(id, cliente_update, db)

@cliente_router.patch("/{id}", response_model=ClienteSalida)
def actualizar_cliente_parcial(id: int, cliente_update: ClienteUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(require_mecanico)):
    return cliente_service.actualizar_cliente_parcial(id, cliente_update, db)

@cliente_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente_logico(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(require_supervisor)):
    return cliente_service.eliminar_cliente_logico(id, db)

