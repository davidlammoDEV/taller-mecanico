from models.proveedor_model import Proveedor
from schemas.proveedor_schema import ProveedorEntrada, ProveedorUpdata
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

def obtener_proveedor(id:int, db:Session):
    proveedor = db.query(Proveedor).filter(Proveedor.id == id, Proveedor.activo == True).first()
    if proveedor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no Encontrado")
    return proveedor

def listar_proveedores(db: Session):
    proveedor = db.query(Proveedor).filter(Proveedor.activo == True).all()
    if len(proveedor) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lista de proveedores vacia")
    return proveedor

def crear_proveedor(proveedor: ProveedorEntrada, db:Session):
    proveedor= Proveedor(documento = proveedor.documento,
                        nombre= proveedor.nombre,
                        nom_empresa = proveedor.nom_empresa,
                        telefono = proveedor.telefono,
                        correo = proveedor.correo)
    db.add(proveedor)
    db.commit()
    db.refresh(proveedor)
    return proveedor

def actualizar_proveedor_completo(id: int, proveedor_update: ProveedorEntrada, db: Session):
    db_proveedor = db.query(Proveedor).filter(Proveedor.id == id).first()
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    for key, value in proveedor_update.model_dump().items():
        setattr(db_proveedor, key, value)

    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

def actualizar_mecanico_parcial(id: int, proveedor_update: ProveedorUpdata, db: Session):
    db_proveedor = db.query(Proveedor).filter(Proveedor.id == id, Proveedor.activo == True).first()

    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado o inactivo")
    update_data = proveedor_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")

    for key, value in update_data.items():
        setattr(db_proveedor, key, value)

    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

def eliminar_proveedor_logico(id: int, db: Session):
    db_proveedor = db.query(Proveedor).filter(Proveedor.id == id, Proveedor.activo==True).first()
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    db_proveedor.activo = False 
    db.commit()
    return None
