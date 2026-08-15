from models.repuesto_model import Repuesto
from schemas.repuesto_schema import RepuestoEntrada, RepuestoUpdata
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

def obtener_repuesto(codigo:str, db:Session):
    repuesto = db.query(Repuesto).filter(Repuesto.codigo == codigo, Repuesto.activo == True).first()
    if repuesto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repuesto no Encontrado")
    return repuesto

def listar_repuestos(db: Session):
    repuesto = db.query(Repuesto).filter(Repuesto.activo == True).all()
    if len(repuesto) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lista de Repuestos vacia")
    return repuesto

def crear_repuesto(repuesto: RepuestoEntrada, db:Session):
    repuesto= Repuesto(codigo = repuesto.codigo,
                        nombre= repuesto.nombre,
                        marca = repuesto.marca,
                        stock = repuesto.stock,
                        costo = repuesto.costo,
                        precio = repuesto.precio,
                        descripcion = repuesto.descripcion,
                        proveedor_id = repuesto.proveedor_id)
    db.add(repuesto)
    db.commit()
    db.refresh(repuesto)
    return repuesto

def actualizar_repuesto_completo(codigo: str, proveedor_update: RepuestoEntrada, db: Session):
    db_repuesto = db.query(Repuesto).filter(Repuesto.codigo == codigo).first()
    if not db_repuesto:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado")

    for key, value in proveedor_update.model_dump().items():
        setattr(db_repuesto, key, value)

    db.commit()
    db.refresh(db_repuesto)
    return db_repuesto

def actualizar_repuesto_parcial(codigo: str, repuesto_updata: RepuestoUpdata, db: Session):
    db_repuesto = db.query(Repuesto).filter(Repuesto.codigo == codigo, Repuesto.activo == True).first()

    if not db_repuesto:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado o inactivo")
    update_data = repuesto_updata.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")

    for key, value in update_data.items():
        setattr(db_repuesto, key, value)

    db.commit()
    db.refresh(db_repuesto)
    return db_repuesto

def eliminar_repuesto_logico(codigo: str, db: Session):
    db_repuesto = db.query(Repuesto).filter(Repuesto.codigo == codigo, Repuesto.activo==True).first()
    if not db_repuesto:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado")
    db_repuesto.activo = False
    db.commit()
    return None
