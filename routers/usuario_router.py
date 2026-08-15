from database.connection import SessionLocal
from schemas.usuarios_schema import *
from services import usuario_service
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from models.usuario_model import Usuario
from tokensitos.auth_dependencias import VerificarRoles, require_supervisor

usuario_router = APIRouter(
    prefix="/usuario",
    tags=["Usuarios"],
    dependencies=[Depends(require_supervisor)]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@usuario_router.get("/{iduser}", response_model=User_Salida)
def obtener_proveedor(iduser:str, db:Session = Depends(get_db)):
    return usuario_service.obtener_Usuario(iduser, db)

@usuario_router.get("/", response_model=List[User_Salida], status_code=status.HTTP_200_OK)
def listar_usuarios(db: Session = Depends(get_db)):
    return usuario_service.listar_usuarios(db)

@usuario_router.post("/", response_model=User_Entrada, status_code=status.HTTP_200_OK)
def crear_proveedor(user: User_Entrada, db:Session = Depends(get_db)):
    return usuario_service.crear_usuario(user, db)

@usuario_router.patch("/{iduser}", response_model=User_Salida)
def actualizar_usuario_parcial(iduser: str, user_update: User_Updata, db: Session = Depends(get_db)):
    return usuario_service.actualizar_usuarios_parcial(iduser, user_update, db)

@usuario_router.delete("/{iduser}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario_logico(iduser: str, db: Session = Depends(get_db)):
    return usuario_service.eliminar_usuario_logico(iduser, db)
