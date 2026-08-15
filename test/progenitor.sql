--  TALLER MECÁNICO — 
--  1. CLIENTE
CREATE TABLE cliente (
    id          SERIAL          PRIMARY KEY,
    documento   VARCHAR(20)     NOT NULL UNIQUE,
    nombre      VARCHAR(100)    NOT NULL,
    telefono    VARCHAR(20),
    correo      VARCHAR(100),
    direccion   VARCHAR(200)
);
--  2. VEHÍCULO
CREATE TABLE vehiculo (
    placa           VARCHAR(10)     PRIMARY KEY,
    marca           VARCHAR(50)     NOT NULL,
    modelo          VARCHAR(50)     NOT NULL,
    ano             INTEGER         NOT NULL,
    color           VARCHAR(30),
    kilometraje     INTEGER         DEFAULT 0,
    observaciones   TEXT,
    cliente_id      INTEGER         NOT NULL
        REFERENCES cliente(id) ON DELETE RESTRICT
);
--  3. MECÁNICO
CREATE TABLE mecanico (
    id              SERIAL          PRIMARY KEY,
    documento       VARCHAR(20)     NOT NULL UNIQUE,
    nombre          VARCHAR(100)    NOT NULL,
    especialidad    VARCHAR(100),
    telefono        VARCHAR(20),
    fecha_ingreso   DATE            NOT NULL DEFAULT CURRENT_DATE,
    estado          VARCHAR(20)     NOT NULL DEFAULT 'Activo'
        CHECK (estado IN ('Activo', 'Inactivo'))
);
--  4. SERVICIO
CREATE TABLE servicio (
    id          SERIAL          PRIMARY KEY,
    nombre      VARCHAR(100)    NOT NULL,
    costo_base  NUMERIC(12,2)   NOT NULL,
    descripcion TEXT
);
--  5. PROVEEDOR
CREATE TABLE proveedor (
    id          SERIAL          PRIMARY KEY,
    documento   VARCHAR(20)     NOT NULL UNIQUE,
    nombre      VARCHAR(100)    NOT NULL,
    nom_empresa VARCHAR(100),
    telefono    VARCHAR(20),
    correo      VARCHAR(100)
);
--  6. REPUESTO
CREATE TABLE repuesto (
    codigo      VARCHAR(20)     PRIMARY KEY,
    nombre      VARCHAR(100)    NOT NULL,
    marca       VARCHAR(50),
    stock       INTEGER         NOT NULL DEFAULT 0,
    costo       NUMERIC(12,2)   NOT NULL,
    precio      NUMERIC(12,2)   NOT NULL,
    descripcion TEXT,
    proveedor_id INTEGER
        REFERENCES proveedor(id) ON DELETE SET NULL
);
--  7. ORDEN DE SERVICIO
CREATE TABLE orden_servicio (
    id              SERIAL          PRIMARY KEY,
    fecha           TIMESTAMP       NOT NULL DEFAULT NOW(),
    diagnostico     TEXT,
    estado          VARCHAR(30)     NOT NULL DEFAULT 'Recibido'
        CHECK (estado IN ('Recibido', 'En Proceso', 'Completado', 'Cancelado')),
    observaciones   TEXT,
    costo_estimado  NUMERIC(12,2),
    cliente_id      INTEGER         NOT NULL
        REFERENCES cliente(id) ON DELETE RESTRICT,
    placa           VARCHAR(10)     NOT NULL
        REFERENCES vehiculo(placa) ON DELETE RESTRICT,
    mecanico_id     INTEGER         NOT NULL
        REFERENCES mecanico(id) ON DELETE RESTRICT
);
--  8. ORDEN ↔ SERVICIO
CREATE TABLE orden_detalle_servicio (
    id              SERIAL          PRIMARY KEY,
    orden_id        INTEGER         NOT NULL
        REFERENCES orden_servicio(id) ON DELETE CASCADE,
    servicio_id     INTEGER         NOT NULL
        REFERENCES servicio(id) ON DELETE RESTRICT,
    cantidad        INTEGER         NOT NULL DEFAULT 1,
    precio_aplicado NUMERIC(12,2)   NOT NULL
);
--  9. ORDEN ↔ REPUESTO  (tabla intermedia)
CREATE TABLE orden_detalle_repuesto (
    id              SERIAL          PRIMARY KEY,
    orden_id        INTEGER         NOT NULL
        REFERENCES orden_servicio(id) ON DELETE CASCADE,
    repuesto_codigo VARCHAR(20)     NOT NULL
        REFERENCES repuesto(codigo) ON DELETE RESTRICT,
    cantidad        INTEGER         NOT NULL DEFAULT 1,
    precio_aplicado NUMERIC(12,2)   NOT NULL
);
--  10. FACTURA
CREATE TABLE factura (
    id          SERIAL          PRIMARY KEY,
    orden_id    INTEGER         NOT NULL UNIQUE
        REFERENCES orden_servicio(id) ON DELETE RESTRICT,
    fecha       TIMESTAMP       NOT NULL DEFAULT NOW(),
    subtotal    NUMERIC(12,2)   NOT NULL,
    impuestos   NUMERIC(12,2)   NOT NULL DEFAULT 0,
    total       NUMERIC(12,2)   NOT NULL,
    cobro_final NUMERIC(12,2)   NOT NULL,
    metodo      VARCHAR(50)     NOT NULL
        CHECK (metodo IN ('Efectivo', 'Pago movil', 'Tarjeta de Débito', 'Transferencia', 'Tarjeta de Crédito'))
);