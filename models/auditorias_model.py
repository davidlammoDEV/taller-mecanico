from sqlalchemy import Column, BigInteger, Integer, String, Text, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from models.base import Base


class Auditoria(Base):
    __tablename__ = "auditoria"

    id = Column(BigInteger, primary_key=True, index=True)
    tabla = Column(String(50), nullable=False, index=True)
    operacion = Column(String(20), nullable=False)  # INSERT, UPDATE, DELETE, CORRECCION_MANUAL
    registro_id = Column(Text, nullable=False, index=True)
    datos_antes = Column(JSONB)
    datos_despues = Column(JSONB)
    usuario_db = Column(Text)
    fecha_evento = Column(TIMESTAMP(timezone=False), index=True)

    # Columnas de revisión del supervisor (ver migracion_auditoria_supervisor.sql)
    revisado = Column(Boolean, default=False)
    nota_supervisor = Column(Text)
    revisado_por = Column(Integer)
    fecha_revision = Column(TIMESTAMP(timezone=False))