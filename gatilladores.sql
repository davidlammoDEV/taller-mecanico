-- ============================================================
-- SCRIPT DE TRIGGERS: AUDITORÍA, VALIDACIÓN Y SINCRONIZACIÓN
-- Tablas: cliente, vehiculo, proveedor, factura
-- muchachos por favor carguen este sript en la base de datos para que los triggers se ejecuten
-- ============================================================

CREATE TABLE IF NOT EXISTS auditoria (
    id BIGSERIAL PRIMARY KEY,
    tabla character varying(50) NOT NULL,
    operacion character varying(10) NOT NULL, -- INSERT, UPDATE, DELETE
    registro_id text NOT NULL,
    datos_antes JSONB,
    datos_despues JSONB,
    usuario_db text DEFAULT current_user,
    fecha_evento timestamp without time zone DEFAULT now()
);


--- Función para registrar auditoría
CREATE OR REPLACE FUNCTION fn_auditoria()
RETURNS TRIGGER AS $$
DECLARE
    v_id text;
BEGIN
    IF TG_OP = 'DELETE' THEN
        v_id := OLD.id::text;
        INSERT INTO auditoria(tabla, operacion, registro_id, datos_antes, datos_despues)
        VALUES (TG_TABLE_NAME, TG_OP, v_id, to_jsonb(OLD), NULL);
        RETURN OLD;
 
    ELSIF TG_OP = 'UPDATE' THEN
        v_id := NEW.id::text;
        INSERT INTO auditoria(tabla, operacion, registro_id, datos_antes, datos_despues)
        VALUES (TG_TABLE_NAME, TG_OP, v_id, to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;
 
    ELSIF TG_OP = 'INSERT' THEN
        v_id := NEW.id::text;
        INSERT INTO auditoria(tabla, operacion, registro_id, datos_antes, datos_despues)
        VALUES (TG_TABLE_NAME, TG_OP, v_id, NULL, to_jsonb(NEW));
        RETURN NEW;
    END IF;
 
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


--tuve que hacer otra funcion para vehiculo porque la llave primaria es placa y no id
CREATE OR REPLACE FUNCTION fn_auditoria_vehiculo()
RETURNS TRIGGER AS $$
DECLARE
    v_id text;
BEGIN
    IF TG_OP = 'DELETE' THEN
        v_id := OLD.placa;
        INSERT INTO auditoria(tabla, operacion, registro_id, datos_antes, datos_despues)
        VALUES (TG_TABLE_NAME, TG_OP, v_id, to_jsonb(OLD), NULL);
        RETURN OLD;
 
    ELSIF TG_OP = 'UPDATE' THEN
        v_id := NEW.placa;
        INSERT INTO auditoria(tabla, operacion, registro_id, datos_antes, datos_despues)
        VALUES (TG_TABLE_NAME, TG_OP, v_id, to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;
 
    ELSIF TG_OP = 'INSERT' THEN
        v_id := NEW.placa;
        INSERT INTO auditoria(tabla, operacion, registro_id, datos_antes, datos_despues)
        VALUES (TG_TABLE_NAME, TG_OP, v_id, NULL, to_jsonb(NEW));
        RETURN NEW;
    END IF;
 
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

--- Crear triggers

DROP TRIGGER IF EXISTS trg_auditoria_cliente ON cliente;
CREATE TRIGGER trg_auditoria_cliente
AFTER INSERT OR UPDATE OR DELETE ON cliente
FOR EACH ROW EXECUTE FUNCTION fn_auditoria();
 
DROP TRIGGER IF EXISTS trg_auditoria_vehiculo ON vehiculo;
CREATE TRIGGER trg_auditoria_vehiculo
AFTER INSERT OR UPDATE OR DELETE ON vehiculo
FOR EACH ROW EXECUTE FUNCTION fn_auditoria_vehiculo();
 
DROP TRIGGER IF EXISTS trg_auditoria_proveedor ON proveedor;
CREATE TRIGGER trg_auditoria_proveedor
AFTER INSERT OR UPDATE OR DELETE ON proveedor
FOR EACH ROW EXECUTE FUNCTION fn_auditoria();
 
DROP TRIGGER IF EXISTS trg_auditoria_factura ON factura;
CREATE TRIGGER trg_auditoria_factura
AFTER INSERT OR UPDATE OR DELETE ON factura
FOR EACH ROW EXECUTE FUNCTION fn_auditoria();

DROP TRIGGER IF EXISTS trg_auditoria_orden_servicio ON orden_servicio;
CREATE TRIGGER trg_auditoria_orden_servicio
AFTER INSERT OR UPDATE OR DELETE ON orden_servicio
FOR EACH ROW EXECUTE FUNCTION fn_auditoria();


---pa las facturas
CREATE OR REPLACE FUNCTION fn_validar_factura()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.subtotal < 0 OR NEW.impuestos < 0 OR NEW.total < 0 THEN
        RAISE EXCEPTION 'Los montos de la factura no pueden ser negativos';
    END IF;
 
    IF NEW.total <> (NEW.subtotal + NEW.impuestos) THEN
        RAISE EXCEPTION 'El total (%) no coincide con subtotal + impuestos (%)',
            NEW.total, (NEW.subtotal + NEW.impuestos);
    END IF;
 
    IF NEW.cobro_final IS NOT NULL AND NEW.cobro_final < 0 THEN
        RAISE EXCEPTION 'El cobro_final no puede ser negativo';
    END IF;
 
    IF NEW.fecha IS NOT NULL AND NEW.fecha > now() THEN
        RAISE EXCEPTION 'La fecha de la factura no puede ser futura';
    END IF;
 
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
 
DROP TRIGGER IF EXISTS trg_validar_factura ON factura;
CREATE TRIGGER trg_validar_factura
BEFORE INSERT OR UPDATE ON factura
FOR EACH ROW EXECUTE FUNCTION fn_validar_factura();

--validar vehiculo
CREATE OR REPLACE FUNCTION fn_validar_vehiculo()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.ano IS NOT NULL AND
       (NEW.ano < 1900 OR NEW.ano > EXTRACT(YEAR FROM CURRENT_DATE)::int + 1) THEN
        RAISE EXCEPTION 'El año del vehículo (%) no es válido', NEW.ano;
    END IF;
 
    IF NEW.kilometraje IS NOT NULL AND NEW.kilometraje < 0 THEN
        RAISE EXCEPTION 'El kilometraje no puede ser negativo';
    END IF;
 
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
 
DROP TRIGGER IF EXISTS trg_validar_vehiculo ON vehiculo;
CREATE TRIGGER trg_validar_vehiculo
BEFORE INSERT OR UPDATE ON vehiculo
FOR EACH ROW EXECUTE FUNCTION fn_validar_vehiculo();

--validar cliente activo para vehiculo
CREATE OR REPLACE FUNCTION fn_validar_cliente_activo_para_vehiculo()
RETURNS TRIGGER AS $$
DECLARE
    v_activo boolean;
BEGIN
    IF NEW.cliente_id IS NOT NULL THEN
        SELECT activo INTO v_activo FROM cliente WHERE id = NEW.cliente_id;
 
        IF v_activo IS NULL THEN
            RAISE EXCEPTION 'El cliente_id % no existe', NEW.cliente_id;
        END IF;
 
        IF v_activo = false THEN
            RAISE EXCEPTION 'No se puede asignar el vehículo a un cliente inactivo (id %)', NEW.cliente_id;
        END IF;
    END IF;
 
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
 
DROP TRIGGER IF EXISTS trg_validar_cliente_activo ON vehiculo;
CREATE TRIGGER trg_validar_cliente_activo
BEFORE INSERT OR UPDATE OF cliente_id ON vehiculo
FOR EACH ROW EXECUTE FUNCTION fn_validar_cliente_activo_para_vehiculo();

--sincronizar vehiculos cuando cliente se desactiva

CREATE OR REPLACE FUNCTION fn_sync_desactivar_vehiculos()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.activo = false AND OLD.activo = true THEN
        UPDATE vehiculo
        SET activo = false
        WHERE cliente_id = NEW.id
          AND activo = true;
    END IF;
 
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
 
DROP TRIGGER IF EXISTS trg_sync_desactivar_vehiculos ON cliente;
CREATE TRIGGER trg_sync_desactivar_vehiculos
AFTER UPDATE OF activo ON cliente
FOR EACH ROW
WHEN (NEW.activo IS DISTINCT FROM OLD.activo)
EXECUTE FUNCTION fn_sync_desactivar_vehiculos();

--orden de servicio 

CREATE OR REPLACE FUNCTION fn_validar_orden_servicio()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.costo_estimado IS NOT NULL AND NEW.costo_estimado < 0 THEN
        RAISE EXCEPTION 'El costo_estimado no puede ser negativo';
    END IF;
 
    IF NEW.fecha IS NOT NULL AND NEW.fecha > now() THEN
        RAISE EXCEPTION 'La fecha de la orden no puede ser futura';
    END IF;
 
    IF NEW.estado IS NOT NULL AND NEW.estado NOT IN
       ('pendiente', 'en_proceso', 'finalizada', 'facturada', 'cancelada') THEN
        RAISE EXCEPTION 'Estado de orden no válido: %', NEW.estado;
    END IF;
 
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
 
DROP TRIGGER IF EXISTS trg_validar_orden_servicio ON orden_servicio;
CREATE TRIGGER trg_validar_orden_servicio
BEFORE INSERT OR UPDATE ON orden_servicio
FOR EACH ROW EXECUTE FUNCTION fn_validar_orden_servicio();

CREATE OR REPLACE FUNCTION fn_sync_factura_orden()
RETURNS TRIGGER AS $$
DECLARE
    v_estado character varying(30);
BEGIN
    SELECT estado INTO v_estado
    FROM orden_servicio
    WHERE id = NEW.orden_id;
 
    IF v_estado IS NULL THEN
        RAISE EXCEPTION 'La orden_id % no existe en orden_servicio', NEW.orden_id;
    END IF;
 
    IF v_estado NOT IN ('finalizada') THEN
        RAISE EXCEPTION
            'No se puede facturar la orden % porque su estado es "%": debe estar "finalizada"',
            NEW.orden_id, v_estado;
    END IF;
 
    UPDATE orden_servicio
    SET estado = 'facturada'
    WHERE id = NEW.orden_id;
 
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
 
DROP TRIGGER IF EXISTS trg_sync_factura_orden ON factura;
CREATE TRIGGER trg_sync_factura_orden
BEFORE INSERT ON factura
FOR EACH ROW EXECUTE FUNCTION fn_sync_factura_orden();
