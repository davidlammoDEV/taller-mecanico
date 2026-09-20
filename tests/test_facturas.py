from datetime import date

def test_listar_facturas(client, auth_headers):
    cliente_datos = {
        "documento": "LISTFAC01",
        "nombre": "Cliente Listar Factura",
        "telefono": "3001112233",
        "correo": "listar@factura.com",
        "direccion": "Calle Listar"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "LISTFAC01")

    vehiculo_datos = {
        "placa": "LISTF01",
        "marca": "Toyota",
        "modelo": "Corolla",
        "ano": 2020,
        "color": "Blanco",
        "kilometraje": 45000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECLISTF01",
        "nombre": "Mecánico Listar Factura",
        "especialidad": "General",
        "telefono": "3009998877",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECLISTF01")

    orden_datos = {
        "fecha": str(date.today()),
        "diagnostico": "Revisión general",
        "estado": "Pendiente",
        "observaciones": "Para facturar",
        "costo_estimado": "150000",
        "cliente_id": cliente_id,
        "placa": "LISTF01",
        "mecanico_id": mecanico_id
    }
    crear_orden = client.post("/orden/", json=orden_datos, headers=auth_headers)
    orden_id = crear_orden.json()["id"]

    client.patch(f"/orden/{orden_id}", json={"estado": "Completado"}, headers=auth_headers)

    factura_datos = {
        "orden_id": orden_id,
        "subtotal": "150000",
        "impuestos": "28500",
        "total": "178500",
        "cobro_final": "178500",
        "metodo": "Efectivo"
    }
    client.post("/factura/", json=factura_datos, headers=auth_headers)

    response = client.get("/factura/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_crear_factura(client, auth_headers):
    cliente_datos = {
        "documento": "CREARFAC01",
        "nombre": "Cliente Crear Factura",
        "telefono": "3002223344",
        "correo": "crear@factura.com",
        "direccion": "Calle Crear"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "CREARFAC01")

    vehiculo_datos = {
        "placa": "CREARF01",
        "marca": "Chevrolet",
        "modelo": "Spark",
        "ano": 2019,
        "color": "Rojo",
        "kilometraje": 30000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECCREARF01",
        "nombre": "Mecánico Crear Factura",
        "especialidad": "Motor",
        "telefono": "3008887766",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECCREARF01")

    orden_datos = {
        "fecha": str(date.today()),
        "diagnostico": "Cambio de aceite",
        "estado": "Pendiente",
        "observaciones": "Para crear factura",
        "costo_estimado": "85000",
        "cliente_id": cliente_id,
        "placa": "CREARF01",
        "mecanico_id": mecanico_id
    }
    crear_orden = client.post("/orden/", json=orden_datos, headers=auth_headers)
    orden_id = crear_orden.json()["id"]

    client.patch(f"/orden/{orden_id}", json={"estado": "Completado"}, headers=auth_headers)

    datos = {
        "orden_id": orden_id,
        "subtotal": "85000",
        "impuestos": "16150",
        "total": "101150",
        "cobro_final": "101150",
        "metodo": "Transferencia"
    }
    response = client.post("/factura/", json=datos, headers=auth_headers)

    assert response.status_code == 201
    assert response.json()["orden_id"] == orden_id
    assert response.json()["metodo"] == "Transferencia"
    assert float(response.json()["total"]) == 101150.0

def test_crear_factura_datos_invalidos(client, auth_headers):
    datos = {
        "subtotal": "100000"
    }
    response = client.post("/factura/", json=datos, headers=auth_headers)
    assert response.status_code == 422

def test_crear_factura_orden_no_completada(client, auth_headers):
    cliente_datos = {
        "documento": "NOCOMP01",
        "nombre": "Cliente No Completada",
        "telefono": "3003334455",
        "correo": "nocomp@factura.com",
        "direccion": "Calle NoComp"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "NOCOMP01")

    vehiculo_datos = {
        "placa": "NOCOMP1",
        "marca": "Mazda",
        "modelo": "3",
        "ano": 2021,
        "color": "Azul",
        "kilometraje": 20000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECNOCOMP01",
        "nombre": "Mecánico NoComp",
        "especialidad": "Frenos",
        "telefono": "3001110000",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECNOCOMP01")

    orden_datos = {
        "fecha": str(date.today()),
        "diagnostico": "Pendiente todavía",
        "estado": "Pendiente",
        "observaciones": "No se puede facturar",
        "costo_estimado": "50000",
        "cliente_id": cliente_id,
        "placa": "NOCOMP1",
        "mecanico_id": mecanico_id
    }
    crear_orden = client.post("/orden/", json=orden_datos, headers=auth_headers)
    orden_id = crear_orden.json()["id"]

    datos = {
        "orden_id": orden_id,
        "subtotal": "50000",
        "impuestos": "9500",
        "total": "59500",
        "cobro_final": "59500",
        "metodo": "Efectivo"
    }
    response = client.post("/factura/", json=datos, headers=auth_headers)
    assert response.status_code == 400
    assert "Solo se puede facturar una orden con estado 'Completado'" in response.json()["detail"]

def test_crear_factura_orden_ya_facturada(client, auth_headers):
    cliente_datos = {
        "documento": "YAFACT01",
        "nombre": "Cliente Ya Facturada",
        "telefono": "3004445566",
        "correo": "yafact@factura.com",
        "direccion": "Calle YaFact"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "YAFACT01")

    vehiculo_datos = {
        "placa": "YAFACT1",
        "marca": "Kia",
        "modelo": "Rio",
        "ano": 2018,
        "color": "Gris",
        "kilometraje": 60000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECYAFACT01",
        "nombre": "Mecánico YaFact",
        "especialidad": "Electricidad",
        "telefono": "3005556677",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECYAFACT01")

    orden_datos = {
        "fecha": str(date.today()),
        "diagnostico": "Ya facturada",
        "estado": "Pendiente",
        "observaciones": "Primera factura",
        "costo_estimado": "120000",
        "cliente_id": cliente_id,
        "placa": "YAFACT1",
        "mecanico_id": mecanico_id
    }
    crear_orden = client.post("/orden/", json=orden_datos, headers=auth_headers)
    orden_id = crear_orden.json()["id"]

    client.patch(f"/orden/{orden_id}", json={"estado": "Completado"}, headers=auth_headers)

    factura_datos = {
        "orden_id": orden_id,
        "subtotal": "120000",
        "impuestos": "22800",
        "total": "142800",
        "cobro_final": "142800",
        "metodo": "Tarjeta de Crédito"
    }
    client.post("/factura/", json=factura_datos, headers=auth_headers)

    response = client.post("/factura/", json=factura_datos, headers=auth_headers)
    assert response.status_code == 400
    assert "Esta orden ya tiene una factura" in response.json()["detail"]

def test_obtener_factura(client, auth_headers):
    cliente_datos = {
        "documento": "GETFAC01",
        "nombre": "Cliente Obtener Factura",
        "telefono": "3006667788",
        "correo": "get@factura.com",
        "direccion": "Calle Get"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "GETFAC01")

    vehiculo_datos = {
        "placa": "GETF01",
        "marca": "Hyundai",
        "modelo": "Accent",
        "ano": 2017,
        "color": "Negro",
        "kilometraje": 80000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECGETF01",
        "nombre": "Mecánico Get Factura",
        "especialidad": "Suspensión",
        "telefono": "3007778899",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECGETF01")

    orden_datos = {
        "fecha": str(date.today()),
        "diagnostico": "Para obtener factura",
        "estado": "Pendiente",
        "observaciones": "Get test",
        "costo_estimado": "200000",
        "cliente_id": cliente_id,
        "placa": "GETF01",
        "mecanico_id": mecanico_id
    }
    crear_orden = client.post("/orden/", json=orden_datos, headers=auth_headers)
    orden_id = crear_orden.json()["id"]

    client.patch(f"/orden/{orden_id}", json={"estado": "Completado"}, headers=auth_headers)

    factura_datos = {
        "orden_id": orden_id,
        "subtotal": "200000",
        "impuestos": "38000",
        "total": "238000",
        "cobro_final": "238000",
        "metodo": "Efectivo"
    }
    crear_factura = client.post("/factura/", json=factura_datos, headers=auth_headers)
    factura_id = crear_factura.json()["id"]

    response = client.get(f"/factura/{factura_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == factura_id
    assert response.json()["orden_id"] == orden_id

def test_obtener_factura_no_existente(client, auth_headers):
    response = client.get("/factura/99999", headers=auth_headers)
    assert response.status_code == 404
    assert "Factura no encontrada" in response.json()["detail"]

def test_obtener_factura_por_orden(client, auth_headers):
    cliente_datos = {
        "documento": "PORORD01",
        "nombre": "Cliente Por Orden",
        "telefono": "3008889900",
        "correo": "pororden@factura.com",
        "direccion": "Calle PorOrden"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "PORORD01")

    vehiculo_datos = {
        "placa": "PORORD1",
        "marca": "Ford",
        "modelo": "Fiesta",
        "ano": 2016,
        "color": "Verde",
        "kilometraje": 95000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECPORORD01",
        "nombre": "Mecánico PorOrden",
        "especialidad": "Transmisión",
        "telefono": "3009990011",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECPORORD01")

    orden_datos = {
        "fecha": str(date.today()),
        "diagnostico": "Por orden",
        "estado": "Pendiente",
        "observaciones": "Buscar por orden",
        "costo_estimado": "175000",
        "cliente_id": cliente_id,
        "placa": "PORORD1",
        "mecanico_id": mecanico_id
    }
    crear_orden = client.post("/orden/", json=orden_datos, headers=auth_headers)
    orden_id = crear_orden.json()["id"]

    client.patch(f"/orden/{orden_id}", json={"estado": "Completado"}, headers=auth_headers)

    factura_datos = {
        "orden_id": orden_id,
        "subtotal": "175000",
        "impuestos": "33250",
        "total": "208250",
        "cobro_final": "208250",
        "metodo": "Tarjeta de Débito"
    }
    client.post("/factura/", json=factura_datos, headers=auth_headers)

    response = client.get(f"/factura/orden/{orden_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["orden_id"] == orden_id

def test_actualizar_factura_parcial(client, auth_headers):
    cliente_datos = {
        "documento": "PATCHFAC01",
        "nombre": "Cliente PATCH Factura",
        "telefono": "3000001122",
        "correo": "patch@factura.com",
        "direccion": "Calle PATCH"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "PATCHFAC01")

    vehiculo_datos = {
        "placa": "PATCHF01",
        "marca": "Nissan",
        "modelo": "Versa",
        "ano": 2022,
        "color": "Blanco",
        "kilometraje": 12000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECPATCHF01",
        "nombre": "Mecánico PATCH Factura",
        "especialidad": "Diagnóstico",
        "telefono": "3001112233",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECPATCHF01")

    orden_datos = {
        "fecha": str(date.today()),
        "diagnostico": "Para PATCH",
        "estado": "Pendiente",
        "observaciones": "Actualizar factura",
        "costo_estimado": "90000",
        "cliente_id": cliente_id,
        "placa": "PATCHF01",
        "mecanico_id": mecanico_id
    }
    crear_orden = client.post("/orden/", json=orden_datos, headers=auth_headers)
    orden_id = crear_orden.json()["id"]

    client.patch(f"/orden/{orden_id}", json={"estado": "Completado"}, headers=auth_headers)

    factura_datos = {
        "orden_id": orden_id,
        "subtotal": "90000",
        "impuestos": "17100",
        "total": "107100",
        "cobro_final": "107100",
        "metodo": "Efectivo"
    }
    crear_factura = client.post("/factura/", json=factura_datos, headers=auth_headers)
    factura_id = crear_factura.json()["id"]

    response = client.patch(
        f"/factura/{factura_id}",
        json={
            "metodo": "Transferencia",
            "cobro_final": "105000"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["metodo"] == "Transferencia"
    assert float(response.json()["cobro_final"]) == 105000.0
    assert float(response.json()["subtotal"]) == 90000.0

def test_eliminar_factura(client, auth_headers):
    cliente_datos = {
        "documento": "DELFAC01",
        "nombre": "Cliente Eliminar Factura",
        "telefono": "3002223344",
        "correo": "del@factura.com",
        "direccion": "Calle Delete"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "DELFAC01")

    vehiculo_datos = {
        "placa": "DELF01",
        "marca": "Renault",
        "modelo": "Sandero",
        "ano": 2015,
        "color": "Gris",
        "kilometraje": 110000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECDELF01",
        "nombre": "Mecánico Delete Factura",
        "especialidad": "General",
        "telefono": "3003334455",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECDELF01")

    orden_datos = {
        "fecha": str(date.today()),
        "diagnostico": "Para eliminar factura",
        "estado": "Pendiente",
        "observaciones": "Se va a borrar la factura",
        "costo_estimado": "60000",
        "cliente_id": cliente_id,
        "placa": "DELF01",
        "mecanico_id": mecanico_id
    }
    crear_orden = client.post("/orden/", json=orden_datos, headers=auth_headers)
    orden_id = crear_orden.json()["id"]

    client.patch(f"/orden/{orden_id}", json={"estado": "Completado"}, headers=auth_headers)

    factura_datos = {
        "orden_id": orden_id,
        "subtotal": "60000",
        "impuestos": "11400",
        "total": "71400",
        "cobro_final": "71400",
        "metodo": "Efectivo"
    }
    crear_factura = client.post("/factura/", json=factura_datos, headers=auth_headers)
    factura_id = crear_factura.json()["id"]

    response = client.delete(f"/factura/{factura_id}", headers=auth_headers)
    assert response.status_code == 204

    response_get = client.get(f"/factura/{factura_id}", headers=auth_headers)
    assert response_get.status_code == 404