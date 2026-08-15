from models.cliente_model import Cliente
from schemas.cliente_schema import ClienteEntrada, ClienteUpdate
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

def obtener_cliente(id:int, db:Session):
    cliente = db.query(Cliente).filter(Cliente.id == id, Cliente.activo == True).first()
    if cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no Encontrado")
    return cliente

def listar_clientes(db: Session):
    return db.query(Cliente).filter(Cliente.activo == True).all()

def crear_cliente(cliente: ClienteEntrada, db: Session):
    try:
        nuevo_cliente = Cliente(
            documento=cliente.documento,
            nombre=cliente.nombre,
            telefono=cliente.telefono,
            correo=cliente.correo,
            direccion=cliente.direccion
        )
        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)
        return nuevo_cliente

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El cliente con documento {cliente.documento} ya se encuentra registrado")

    except DataError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uno o más campos superan la longitud máxima de caracteres permitida")

def actualizar_cliente_completo(id: int, cliente_update: ClienteEntrada, db: Session):
    db_cliente = db.query(Cliente).filter(Cliente.id == id, Cliente.activo == True).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado o inactivo")

    try:
        for key, value in cliente_update.model_dump().items():
            setattr(db_cliente, key, value)

        db.commit()
        db.refresh(db_cliente)
        return db_cliente

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El documento {cliente_update.documento} ya está registrado por otro cliente")

    except DataError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uno o más campos superan la longitud máxima permitida.")


def actualizar_cliente_parcial(id: int, cliente_update: ClienteUpdate, db: Session):
    db_cliente = db.query(Cliente).filter(Cliente.id == id, Cliente.activo == True).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado o inactivo")

    update_data = cliente_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")

    try:
        for key, value in update_data.items():
            setattr(db_cliente, key, value)

        db.commit()
        db.refresh(db_cliente)
        return db_cliente

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El documento o correo ingresado ya pertenece a otro cliente")
    except DataError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uno o más campos superan la longitud máxima permitida.")

def eliminar_cliente_logico(id: int, db: Session):
    db_cliente = db.query(Cliente).filter(Cliente.id == id, Cliente.activo==True).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    # Aki en lugar de db.delete(db_cliente), hacemos que ese maldito cambie su estado civil a desaperecido
    db_cliente.activo = False
    db.commit()
    return None

