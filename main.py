from fastapi import FastAPI
from database.connection import engine
from models.base import Base

from models.cliente_model import Cliente
from models.vehiculo_model import Vehiculo
from models.mecanico_model import Mecanico
from models.supervisor_model import Supervisor
from models.servicio_model import Servicio
from models.proveedor_model import Proveedor
from models.repuesto_model import Repuesto
from models.factura_model import Factura
from models.orden_model import Orden
from models.ordenDetalleRepuesto_model import OrdenDetalleRepuesto
from models.ordenDetalleServicio_model import OrdenDetalleServicio
from models.usuario_model import Usuario
from models.rol_model import Rol
from models.user_login_model import User_Log
from models.refresh_token_model import RefreshToken
from models.auditorias_model import Auditoria


Base.metadata.create_all(bind=engine)

from routers.cliente_router import cliente_router
from routers.vehiculo_router import vehiculo_router
from routers.mecanico_router import mecanico_router
from routers.supervisor_router import supervisor_router
from routers.servicio_router import servicio_router
from routers.proveedor_router import proveedor_router
from routers.repuesto_router import repuesto_router
from routers.factura_router import factura_router
from routers.orden_router import orden_router
from routers.usuario_router import usuario_router
from routers.rol_router import rol_router
from routers.user_log_router import user_log_router
from tokensitos.auth_router import router as auth_router
from routers.auditorias import router as auditoria_router

app = FastAPI(
    title="API Taller Mecánico",
    description="Sistema para el Taller mecanico",
    version="1.0.0"
)

app.include_router(cliente_router)
app.include_router(vehiculo_router)
app.include_router(mecanico_router)
app.include_router(supervisor_router)
app.include_router(servicio_router)
app.include_router(proveedor_router)
app.include_router(repuesto_router)
app.include_router(factura_router)
app.include_router(orden_router)
app.include_router(usuario_router)
app.include_router(rol_router)
app.include_router(user_log_router)
app.include_router(auth_router)
app.include_router(auditoria_router)

@app.get("/")
def index():
    return "bienvenido"
