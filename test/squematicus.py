from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict
 
 
#  CLIENTE
 
class ClienteBase(BaseModel):
    documento: str = Field(..., max_length=20, examples=["10203040"])
    nombre: str = Field(..., max_length=100, examples=["Carlos Pérez"])
    telefono: Optional[str] = Field(None, max_length=20, examples=["3001234567"])
    correo: Optional[EmailStr] = Field(None, examples=["carlos@email.com"])
    direccion: Optional[str] = Field(None, max_length=200, examples=["Calle 45 #12-34"])
 
 
class ClienteCreate(ClienteBase):
    pass
 
 
class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[EmailStr] = None
    direccion: Optional[str] = Field(None, max_length=200)
 
 
class ClienteResponse(ClienteBase):
    id: int
 
    model_config = ConfigDict(from_attributes=True)
 
 
class ClienteConVehiculos(ClienteResponse):
    vehiculos: List["VehiculoResponse"] = []
 
 
#  VEHiCULO

 
class VehiculoBase(BaseModel):
    placa: str = Field(..., max_length=10, examples=["ABC123"])
    marca: str = Field(..., max_length=50, examples=["Toyota"])
    modelo: str = Field(..., max_length=50, examples=["Corolla"])
    ano: int = Field(..., ge=1900, le=2100, examples=[2022])
    color: Optional[str] = Field(None, max_length=30, examples=["Gris"])
    kilometraje: int = Field(default=0, ge=0, examples=[15000])
    observaciones: Optional[str] = Field(None, examples=["Sin choques previos"])
    cliente_id: int = Field(..., examples=[1])
 
 
class VehiculoCreate(VehiculoBase):
    pass
 
 
class VehiculoUpdate(BaseModel):
    marca: Optional[str] = Field(None, max_length=50)
    modelo: Optional[str] = Field(None, max_length=50)
    ano: Optional[int] = Field(None, ge=1900, le=2100)
    color: Optional[str] = Field(None, max_length=30)
    kilometraje: Optional[int] = Field(None, ge=0)
    observaciones: Optional[str] = None
 
 
class VehiculoResponse(VehiculoBase):
    model_config = ConfigDict(from_attributes=True)
 
 
#  MECÁNICO adeptus
 
EstadoMecanico = str  # 'Activo' | 'Inactivo'
 
 
class MecanicoBase(BaseModel):
    documento: str = Field(..., max_length=20, examples=["708090"])
    nombre: str = Field(..., max_length=100, examples=["Luis Torres"])
    especialidad: Optional[str] = Field(None, max_length=100, examples=["Motores y Suspensión"])
    telefono: Optional[str] = Field(None, max_length=20, examples=["3201112233"])
    fecha_ingreso: date = Field(default_factory=date.today)
    estado: EstadoMecanico = Field(default="Activo", examples=["Activo"])
 
 
class MecanicoCreate(MecanicoBase):
    pass
 
 
class MecanicoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    especialidad: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    estado: Optional[EstadoMecanico] = None
 
 
class MecanicoResponse(MecanicoBase):
    id: int
 
    model_config = ConfigDict(from_attributes=True)

 
#  SERVICIO
 
class ServicioBase(BaseModel):
    nombre: str = Field(..., max_length=100, examples=["Cambio de Aceite"])
    costo_base: Decimal = Field(..., gt=0, decimal_places=2, examples=[50000.00])
    descripcion: Optional[str] = Field(None, examples=["Cambio de aceite sintético y filtro"])
 
class ServicioCreate(ServicioBase):
    pass
 
class ServicioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    costo_base: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    descripcion: Optional[str] = None
 
 
class ServicioResponse(ServicioBase):
    id: int
 
    model_config = ConfigDict(from_attributes=True)
 
 
# tengo que decir que tengo miedo de que la ia adivine lo que voy a hacer alluda
#  PROVEEDOR
 
class ProveedorBase(BaseModel):
    documento: str = Field(..., max_length=20, examples=["900100"])
    nombre: str = Field(..., max_length=100, examples=["Juan Repuestos"])
    nom_empresa: Optional[str] = Field(None, max_length=100, examples=["Autopartes Global"])
    telefono: Optional[str] = Field(None, max_length=20, examples=["6015550000"])
    correo: Optional[EmailStr] = Field(None, examples=["ventas@autopartes.com"])
 
class ProveedorCreate(ProveedorBase):
    pass
 
class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    nom_empresa: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[EmailStr] = None
 
class ProveedorResponse(ProveedorBase):
    id: int
 
    model_config = ConfigDict(from_attributes=True)
 
 
#  REPUESTO (desaprubo esta lista porque los componentes no fueron adquiridos en maracay)

 
class RepuestoBase(BaseModel):
    codigo: str = Field(..., max_length=20, examples=["FIL-001"])
    nombre: str = Field(..., max_length=100, examples=["Filtro de Aceite"])
    marca: Optional[str] = Field(None, max_length=50, examples=["Bosch"])
    stock: int = Field(default=0, ge=0, examples=[50])
    costo: Decimal = Field(..., gt=0, decimal_places=2, examples=[15000.00])
    precio: Decimal = Field(..., gt=0, decimal_places=2, examples=[25000.00])
    descripcion: Optional[str] = Field(None, examples=["Filtro de alto rendimiento"])
    proveedor_id: Optional[int] = Field(None, examples=[1])
 
 
class RepuestoCreate(RepuestoBase):
    pass
 
 
class RepuestoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    marca: Optional[str] = Field(None, max_length=50)
    stock: Optional[int] = Field(None, ge=0)
    costo: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    precio: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    descripcion: Optional[str] = None
    proveedor_id: Optional[int] = None
 
 
class RepuestoResponse(RepuestoBase):
    proveedor: Optional[ProveedorResponse] = None
 
    model_config = ConfigDict(from_attributes=True)
 
#  ORDEN nexus SERVICIO  
 
class OrdenDetalleServicioBase(BaseModel):
    servicio_id: int = Field(..., examples=[1])
    cantidad: int = Field(default=1, ge=1, examples=[1])
    precio_aplicado: Decimal = Field(..., gt=0, decimal_places=2, examples=[50000.00])
 
 
class OrdenDetalleServicioCreate(OrdenDetalleServicioBase):
    pass
 
 
class OrdenDetalleServicioResponse(OrdenDetalleServicioBase):
    id: int
    servicio: ServicioResponse
 
    model_config = ConfigDict(from_attributes=True)
 
 
#  ORDEN conectier REPUESTO  (detalle intermedio) 
class OrdenDetalleRepuestoBase(BaseModel):
    repuesto_codigo: str = Field(..., max_length=20, examples=["FIL-001"])
    cantidad: int = Field(default=1, ge=1, examples=[1])
    precio_aplicado: Decimal = Field(..., gt=0, decimal_places=2, examples=[25000.00])
 
 
class OrdenDetalleRepuestoCreate(OrdenDetalleRepuestoBase):
    pass
 
 
class OrdenDetalleRepuestoResponse(OrdenDetalleRepuestoBase):
    id: int
    repuesto: RepuestoResponse
 
    model_config = ConfigDict(from_attributes=True)
 
 

#  ORDEN DE SERVICIO
 
EstadoOrden = str  # 'entregado' | 'En Proceso' | 'Completado' | 'Cancelado'
 
 
class OrdenServicioBase(BaseModel):
    diagnostico: Optional[str] = Field(None, examples=["Ruido metálico en motor"])
    estado: EstadoOrden = Field(default="Recibido", examples=["Recibido"])
    observaciones: Optional[str] = Field(None, examples=["Se sugiere cambio de aceite inmediato"])
    costo_estimado: Optional[Decimal] = Field(None, ge=0, decimal_places=2, examples=[75000.00])
    cliente_id: int = Field(..., examples=[1])
    placa: str = Field(..., max_length=10, examples=["ABC123"])
    mecanico_id: int = Field(..., examples=[1])
 
 
class OrdenServicioCreate(OrdenServicioBase):
    servicios: List[OrdenDetalleServicioCreate] = []
    repuestos: List[OrdenDetalleRepuestoCreate] = []
 
 
class OrdenServicioUpdate(BaseModel):
    diagnostico: Optional[str] = None
    estado: Optional[EstadoOrden] = None
    observaciones: Optional[str] = None
    costo_estimado: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    mecanico_id: Optional[int] = None
 
 
class OrdenServicioResponse(OrdenServicioBase):
    id: int
    fecha: datetime
    cliente: ClienteResponse
    vehiculo: VehiculoResponse
    mecanico: MecanicoResponse
    servicios: List[OrdenDetalleServicioResponse] = []
    repuestos: List[OrdenDetalleRepuestoResponse] = []
 
    model_config = ConfigDict(from_attributes=True)
 
 
class OrdenServicioResumen(BaseModel):
    """Vista resumida para listados (sin detalles anidados)."""
    id: int
    fecha: datetime
    estado: EstadoOrden
    costo_estimado: Optional[Decimal]
    cliente: ClienteResponse
    placa: str
 
    model_config = ConfigDict(from_attributes=True)
 
#  FACTUradpr

 
MetodoPago = str  # 'Efectivo' | 'Tarjeta de Crédito' | 'Tarjeta de Débito' | 'Transferencia'
 
 
class FacturaBase(BaseModel):
    orden_id: int = Field(..., examples=[1])
    subtotal: Decimal = Field(..., ge=0, decimal_places=2, examples=[63025.21])
    impuestos: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2, examples=[11974.79])
    total: Decimal = Field(..., ge=0, decimal_places=2, examples=[75000.00])
    cobro_final: Decimal = Field(..., ge=0, decimal_places=2, examples=[75000.00])
    metodo: MetodoPago = Field(..., examples=["Tarjeta de Crédito"])
 
 
class FacturaCreate(FacturaBase):
    pass
 
 
class FacturaUpdate(BaseModel):
    subtotal: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    impuestos: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    total: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    cobro_final: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    metodo: Optional[MetodoPago] = None
 
 
class FacturaResponse(FacturaBase):
    id: int
    fecha: datetime
    orden: OrdenServicioResumen
 
    model_config = ConfigDict(from_attributes=True)
 
 

#  Resolución de referencias circulares
#  (necesario porque ClienteConVehiculos → VehiculoResponse)
 
ClienteConVehiculos.model_rebuild()