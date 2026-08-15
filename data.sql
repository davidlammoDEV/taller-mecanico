BEGIN;

-- ========================================================
-- 1. CLIENTES (Tablas independientes)
-- ========================================================
INSERT INTO public.cliente (id, documento, nombre, telefono, correo, direccion, activo) VALUES
(1, 'V-18234567', 'Carlos Eduardo Mendoza', '0414-7123456', 'carlos.mendoza@email.com', 'Av. Principal San Cristóbal, Casa #45', true),
(2, 'V-20112334', 'María Alejandra Gómez', '0424-7654321', 'maria.gomez@email.com', 'Barrio Obrero, Calle 10 con Carrera 19', true),
(3, 'J-30987654', 'Inversiones Los Andes C.A.', '0276-3456789', 'contacto@losandes.com', 'Zona Industrial Las Lomas, Galpón 12', true),
(4, 'V-15678901', 'Roberto José Silva', '0412-5554321', 'roberto.silva@email.com', 'Pueblo Nuevo, Urb. Pirineos, Res. El Parral', true);

-- ========================================================
-- 2. MECÁNICOS
-- ========================================================
INSERT INTO public.mecanico (id, documento, nombre, especialidad, telefono, fecha_ingreso, activo) VALUES
(1, 'V-14556778', 'José Luis Hernández', 'Electricidad y Diagnóstico por Escáner', '0414-9876543', '2021-03-15', true),
(2, 'V-17889001', 'Pedro Antonio Ramírez', 'Mecánica General y Motores', '0424-1112233', '2022-06-01', true),
(3, 'V-19334556', 'Miguel Ángel Torres', 'Frenos y Suspensión', '0412-3334455', '2023-01-10', true);

-- ========================================================
-- 3. PROVEEDORES
-- ========================================================
INSERT INTO public.proveedor (id, documento, nombre, nom_empresa, telefono, correo, activo) VALUES
(1, 'J-12345678', 'Jesús Benítez', 'AutoRepuestos El Galpón C.A.', '0276-5551234', 'ventas@elgalpon.com', true),
(2, 'J-87654321', 'Distribuidora Japonesa', 'Repuestos y Partes Nippon S.A.', '0212-9998877', 'contacto@nipponparts.com', true);

-- ========================================================
-- 4. SERVICIOS
-- ========================================================
INSERT INTO public.servicio (id, nombre, costo_base, descripcion, activo) VALUES
(1, 'Mantenimiento Preventivo Básico', 45.00, 'Cambio de aceite, filtro de aceite y revisión de puntos de seguridad', true),
(2, 'Alineación y Balanceo', 25.00, 'Alineación láser de tren delantero y balanceo de 4 ruedas', true),
(3, 'Diagnóstico Computarizado', 30.00, 'Escaneo de códigos de falla OBD2 y revisión de sensores', true),
(4, 'Mantenimiento Sistema de Frenos', 50.00, 'Limpieza, rectificado de discos y cambio de pastillas', true);

-- ========================================================
-- 5. VEHÍCULOS
-- ========================================================
INSERT INTO public.vehiculo (placa, marca, modelo, ano, color, kilometraje, observaciones, activo, cliente_id) VALUES
('AB123CD', 'Toyota', 'Corolla 1.8', 2015, 'Gris Plata', 145000, 'Detalle menor de pintura en parachoques trasero', true, 1),
('A89BC1D', 'Chevrolet', 'Cruze 1.8', 2013, 'Blanco', 112000, 'Presenta bote leve de aceite por tapa válvula', true, 2),
('A11XY00', 'Ford', 'Explorer 3.5', 2018, 'Negro', 88000, 'Vehículo de flota corporativa', true, 3),
('AA555ZZ', 'Hyundai', 'Tucson 2.0', 2011, 'Azul', 180000, 'Requiere revisión de tren delantero', true, 4);

-- ========================================================
-- 6. REPUESTOS
-- ========================================================
INSERT INTO public.repuesto (codigo, nombre, marca, stock, costo, precio, descripcion, activo, proveedor_id) VALUES
('REP-FIL-001', 'Filtro de Aceite Sintético', 'WIX', 25, 6.00, 12.00, 'Filtro de aceite de alto rendimiento', true, 1),
('REP-ACE-002', 'Aceite Semi-Sintético 15W40 (Galón)', 'Shell', 15, 22.00, 35.00, 'Aceite Shell Helix HX7 15W-40', true, 1),
('REP-PAS-003', 'Pastillas de Freno Delanteras', 'Bosch', 8, 28.00, 48.00, 'Juego de pastillas cerámicas de alto frenado', true, 2),
('REP-BUJ-004', 'Bujía de Iridio (Unidad)', 'NGK', 40, 5.50, 10.00, 'Bujía NGK Laser Iridium', true, 2);

-- ========================================================
-- 7. ÓRDENES DE SERVICIO
-- ========================================================
INSERT INTO public.orden_servicio (id, fecha, diagnostico, estado, observaciones, costo_estimado, cliente_id, placa, mecanico_id, activo) VALUES
(1, '2026-07-20 09:30:00', 'Ruido en frenos delanteros y servicio de rutina', 'Completado', 'Cliente reporta chillido al frenar', 95.00, 1, 'AB123CD', 3, true),
(2, '2026-07-25 14:15:00', 'Luz de Check Engine encendida y pérdida de potencia', 'En Proceso', 'Sensor de oxígeno con fallas de lectura', 120.00, 2, 'A89BC1D', 1, true),
(3, '2026-07-26 10:00:00', 'Mantenimiento de 90,000 km y alineación', 'Pendiente', 'Pendiente por confirmación de repuestos', 80.00, 3, 'A11XY00', 2, true);

-- ========================================================
-- 8. DETALLES DE LA ÓRDEN (Servicios y Repuestos)
-- ========================================================
-- Detalle de Servicios contratados
INSERT INTO public.orden_detalle_servicio (id, orden_id, servicio_id, cantidad, precio_aplicado) VALUES
(1, 1, 1, 1, 45.00), -- Mantenimiento preventivo en Orden 1
(2, 1, 4, 1, 50.00), -- Servicio de frenos en Orden 1
(3, 2, 3, 1, 30.00); -- Diagnóstico computarizado en Orden 2

-- Detalle de Repuestos consumidos
INSERT INTO public.orden_detalle_repuesto (id, orden_id, repuesto_codigo, cantidad, precio_aplicado) VALUES
(1, 1, 'REP-FIL-001', 1, 12.00), -- 1 Filtro de aceite en Orden 1
(2, 1, 'REP-ACE-002', 1, 35.00), -- 1 Galón de aceite en Orden 1
(3, 1, 'REP-PAS-003', 1, 48.00); -- Pastillas de freno en Orden 1

-- ========================================================
-- 9. FACTURAS
-- ========================================================
INSERT INTO public.factura (id, orden_id, fecha, subtotal, impuestos, total, cobro_final, metodo, activo) VALUES
(1, 1, '2026-07-21 11:00:00', 190.00, 30.40, 220.40, 220.40, 'Transferencia', true);

-- ========================================================
-- 10. REINICIO DE SECUENCIAS
-- ========================================================
SELECT setval('public.cliente_id_seq', (SELECT MAX(id) FROM public.cliente));
SELECT setval('public.mecanico_id_seq', (SELECT MAX(id) FROM public.mecanico));
SELECT setval('public.proveedor_id_seq', (SELECT MAX(id) FROM public.proveedor));
SELECT setval('public.servicio_id_seq', (SELECT MAX(id) FROM public.servicio));
SELECT setval('public.orden_servicio_id_seq', (SELECT MAX(id) FROM public.orden_servicio));
SELECT setval('public.orden_detalle_servicio_id_seq', (SELECT MAX(id) FROM public.orden_detalle_servicio));
SELECT setval('public.orden_detalle_repuesto_id_seq', (SELECT MAX(id) FROM public.orden_detalle_repuesto));
SELECT setval('public.factura_id_seq', (SELECT MAX(id) FROM public.factura));

COMMIT;