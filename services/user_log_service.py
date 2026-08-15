from models.user_login_model import User_Log
from models.usuario_model import Usuario
from models.rol_model import Rol
from schemas.user_login_schema import User_LogEntrada, User_LogUpdata
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status, HTTPException

def listar_usuarios_rol(db: Session):
    listar_rol = db.query(User_Log).filter(User_Log.activo == True).all()

    if not listar_rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No se encontraron relaciones de usuario-rol activas"
        )
    return listar_rol


def crear_usuario_rol(userol: User_LogEntrada, db: Session):
    
    existe_usuario = db.query(Usuario).filter(Usuario.iduser == userol.iduser).first()
    if not existe_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El usuario con ID '{userol.iduser}' no existe"
        )

    existe_rol = db.query(Rol).filter(Rol.idrol == userol.idrol).first()
    if not existe_rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El rol con ID '{userol.idrol}' no existe"
        )

    try:
        nuevo_userol = User_Log(
            iduser=userol.iduser,
            idrol=userol.idrol,
            activo=True
        )
        db.add(nuevo_userol)
        db.commit()
        db.refresh(nuevo_userol)
        return nuevo_userol
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad: Este usuario ya tiene una asignación de rol activa o los datos ingresados son erróneos."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ocurrió un error al procesar la solicitud: {str(e)}"
        )


def actualizar_usuario_rol_parcial(iduser_log: int, userlog_updata: User_LogUpdata, db: Session):
    db_userlog = db.query(User_Log).filter(User_Log.iduser_log == iduser_log, User_Log.activo == True).first()
    if not db_userlog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Registro de Usuario-Rol con ID {iduser_log} no fue encontrado"
        )

    update_data = userlog_updata.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se enviaron campos válidos para actualizar"
        )

    if "idrol" in update_data:
        existe_rol = db.query(Rol).filter(Rol.idrol == update_data["idrol"]).first()
        if not existe_rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El nuevo rol con ID {update_data['idrol']} no existe"
            )

    try:
        for key, value in update_data.items():
            setattr(db_userlog, key, value)

        db.commit()
        db.refresh(db_userlog)
        return db_userlog
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los datos proporcionados violan una restricción de la base de datos."
        )


def eliminar_usuario_rol_logico(iduser_log: int, db: Session):
    db_userlog = db.query(User_Log).filter(User_Log.iduser_log == iduser_log, User_Log.activo == True).first()
    if not db_userlog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No se encontró el registro Usuario-Rol con ID {iduser_log} para eliminar"
        )
        
    try:
        db_userlog.activo = False
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo realizar el borrado lógico del registro"
        )