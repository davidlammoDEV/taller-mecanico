from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from database.connection import get_db
from models.rol_model import Rol
from models.usuario_model import Usuario
from tokensitos.tokensificador import decodificar_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decodificar_access_token(token)
        correo: str = payload.get("sub")
        if correo is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.correo == correo).first()
    if user is None or not user.activo:
        raise credentials_exception

    return user


class VerificarRoles:
    def __init__(self, roles_permitidos: list[int | str]):
        self.roles_permitidos = roles_permitidos

    def _tiene_rol_permitido(self, user: Usuario, db: Session) -> bool:
        if not user.login_data or not user.login_data.activo:
            return False

        rol_id = user.login_data.idrol
        if rol_id is None:
            return False

        for rol_permitido in self.roles_permitidos:
            if isinstance(rol_permitido, int) and rol_id == rol_permitido:
                return True

            if isinstance(rol_permitido, str):
                rol_db = db.query(Rol).filter(Rol.idrol == rol_id).first()
                if rol_db and rol_db.nombre.lower() == rol_permitido.lower():
                    return True

        return False

    def __call__(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
        exception_credenciales = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = decodificar_access_token(token)
            correo: str = payload.get("sub")
            if correo is None:
                raise exception_credenciales
        except JWTError:
            raise exception_credenciales

        user = db.query(Usuario).filter(Usuario.correo == correo).first()

        if user is None or not user.activo:
            raise exception_credenciales

        if not user.login_data or not user.login_data.activo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El acceso de este usuario se encuentra inactivo."
            )

        if not self._tiene_rol_permitido(user, db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes los permisos necesarios para acceder a esta sección."
            )

        return user


require_supervisor = VerificarRoles(["supervisor"])
require_mecanico = VerificarRoles(["mecanico", "supervisor"])
require_cliente = VerificarRoles(["cliente", "mecanico", "supervisor",]) 