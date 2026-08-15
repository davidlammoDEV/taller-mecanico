from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.connection import get_db
from schemas.user_login_schema import User_LogEntrada, User_LogUpdata
import services.user_log_service as user_login_service
from tokensitos.auth_dependencias import VerificarRoles, require_supervisor

user_log_router = APIRouter(
    prefix="/usuarios-roles",
    tags=["Gestión de Roles de Usuario"],
    dependencies=[Depends(require_supervisor)]
)

@user_log_router.get("/", status_code=status.HTTP_200_OK)
def listar_usuarios_rol(db: Session = Depends(get_db)):
    return user_login_service.listar_usuarios_rol(db)

@user_log_router.post("/", status_code=status.HTTP_201_CREATED)
def crear_usuario_rol(userol: User_LogEntrada, db: Session = Depends(get_db)):
    return user_login_service.crear_usuario_rol(userol, db)

@user_log_router.patch("/{iduser_log}", status_code=status.HTTP_200_OK)
def actualizar_usuario_rol(
    iduser_log: int,
    userlog_updata: User_LogUpdata,
    db: Session = Depends(get_db)
):
    return user_login_service.actualizar_usuario_rol_parcial(iduser_log, userlog_updata, db)


@user_log_router.delete("/{iduser_log}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario_rol(iduser_log: int, db: Session = Depends(get_db)):
    return user_login_service.eliminar_usuario_rol_logico(iduser_log, db)