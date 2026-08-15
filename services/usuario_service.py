from models.usuario_model import Usuario
from schemas.usuarios_schema import User_Entrada, User_Salida, User_Updata
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from tokensitos.tokensificador import hashear_password

def obtener_Usuario(iduser:str, db:Session):
    usua = db.query(Usuario).filter(Usuario.iduser == iduser, Usuario.activo == True).first()
    if usua is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no Encontrado")
    return usua

def listar_usuarios(db: Session):
    usua = db.query(Usuario).filter(Usuario.activo == True).all()
    if len(usua) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lista de usuarios vacia")
    return usua

def crear_usuario(user: User_Entrada, db: Session):
    usuario_db = Usuario(
        iduser=user.iduser,
        nombre=user.nombre,
        apellido=user.apellido,
        correo=user.correo,
        contrase=hashear_password(user.contrase) 
    )
    db.add(usuario_db)
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

def actualizar_usuarios_parcial(iduser: str, usuario_update: User_Updata, db: Session):
    db_usuario = db.query(Usuario).filter(Usuario.iduser == iduser, Usuario.activo == True).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_data = usuario_update.model_dump(exclude_unset=True)
    
    # 3. Si se incluye la contraseña en la actualización, la hasheamos antes de guardarla
    if "contrase" in update_data and update_data["contrase"]:
        update_data["contrase"] = hashear_password(update_data["contrase"])

    for key, value in update_data.items():
        setattr(db_usuario, key, value)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def eliminar_usuario_logico(iduser: str, db: Session):
    db_user = db.query(Usuario).filter(Usuario.iduser == iduser, Usuario.activo==True).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_user.activo = False
    db.commit()
    return None

