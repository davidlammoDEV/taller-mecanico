from database.connection import SessionLocal
from schemas.factura_schema import FacturaActualizar, FacturaEntrada, FacturaSalida
from services import factura_service
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from models.usuario_model import Usuario
from tokensitos.auth_dependencias import VerificarRoles

factura_router = APIRouter(
    prefix="/factura",
    tags=["Factura"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@factura_router.get("/{factura_id}", response_model=FacturaSalida)
def obtener_factura(factura_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3])) ):
    return factura_service.obtener_factura(factura_id, db)

@factura_router.get("/", response_model=List[FacturaSalida], status_code=status.HTTP_200_OK)
def listar_facturas(db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return factura_service.listar_facturas(db)

@factura_router.get("/orden/{orden_id}", response_model=FacturaSalida)
def obtener_factura_por_orden(orden_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return factura_service.obtener_factura_por_orden(orden_id, db)

@factura_router.post("/", response_model=FacturaSalida, status_code=status.HTTP_201_CREATED)
def crear_factura(factura: FacturaEntrada, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return factura_service.crear_factura(factura, db)

@factura_router.patch("/{factura_id}", response_model=FacturaSalida)
def actualizar_factura_parcial(factura_id: int, factura_update: FacturaActualizar, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return factura_service.actualizar_factura_parcial(factura_id, factura_update, db)

@factura_router.delete("/{factura_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_factura_logica(factura_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(VerificarRoles([1,2,3]))):
    return factura_service.eliminar_factura_logica(factura_id, db)