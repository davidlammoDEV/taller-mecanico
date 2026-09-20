from datetime import date

def test_listar_ordenes(client, auth_headers):
    cliente_datos = {
        "documento": "LISTORD01",
        "nombre": "Cliente Listar Orden",
        "telefono": "3001112233",
        "correo": "listar@orden.com",
        "direccion": "Calle Listar"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "LISTORD01")

    vehiculo_datos = {
        "placa": "LIST01",
        "marca": "Toyota",
        "modelo": "Corolla",
        "ano": 2020,
        "color": "Blanco",
        "kilometraje": 45000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECLIST01",
        "nombre": "Mecánico Listar",
        "especialidad": "General",
        "telefono": "3009998877",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECLIST01")

    orden_datos = {
        "fecha": str(date.today()),
        "diagnostico": "Revisión general",
        "estado": "Pendiente",
        "observaciones": "Orden para listar",
        "costo_estimado": "100000",
        "cliente_id": cliente_id,
        "placa": "LIST01",
        "mecanico_id": mecanico_id
    }
    client.post("/orden/", json=orden_datos, headers=auth_headers)

    response = client.get("/orden/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_crear_orden(client, auth_headers):
    cliente_datos = {
        "documento": "CREARORD01",
        "nombre": "Cliente Crear Orden",
        "telefono": "3002223344",
        "correo": "crear@orden.com",
        "direccion": "Calle Crear"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "CREARORD01")

    vehiculo_datos = {
        "placa": "CREAR01",
        "marca": "Chevrolet",
        "modelo": "Spark",
        "ano": 2019,
        "color": "Rojo",
        "kilometraje": 30000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECCREAR01",
        "nombre": "Mecánico Crear",
        "especialidad": "Motor",
        "telefono": "3008887766",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECCREAR01")

    datos = {
        "fecha": str(date.today()),
        "diagnostico": "Cambio de aceite y filtros",
        "estado": "Pendiente",
        "observaciones": "Cliente solicitó revisión completa",
        "costo_estimado": "85000.50",
        "cliente_id": cliente_id,
        "placa": "CREAR01",
        "mecanico_id": mecanico_id
    }
    response = client.post("/orden/", json=datos, headers=auth_headers)

    assert response.status_code == 201
    assert response.json()["diagnostico"] == "Cambio de aceite y filtros"
    assert response.json()["estado"] == "Pendiente"
    assert response.json()["placa"] == "CREAR01"
    assert response.json()["cliente_id"] == cliente_id
    assert response.json()["mecanico_id"] == mecanico_id

def test_crear_orden_datos_invalidos(client, auth_headers):
    datos = {
        "diagnostico": "Solo diagnóstico"
    }
    response = client.post("/orden/", json=datos, headers=auth_headers)
    assert response.status_code == 422

def test_crear_orden_cliente_no_existente(client, auth_headers):
    cliente_datos = {
        "documento": "FKCLIENTE",
        "nombre": "Cliente Temporal",
        "telefono": "3000000000",
        "correo": "fk@orden.com",
        "direccion": "Temporal"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "FKCLIENTE")

    vehiculo_datos = {
        "placa": "FK001",
        "marca": "Mazda",
        "modelo": "3",
        "ano": 2021,
        "color": "Azul",
        "kilometraje": 20000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECFK01",
        "nombre": "Mecánico FK",
        "especialidad": "Frenos",
        "telefono": "3001110000",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECFK01")

    datos = {
        "fecha": str(date.today()),
        "diagnostico": "Prueba FK",
        "estado": "Pendiente",
        "observaciones": "Cliente no existe",
        "costo_estimado": "10000",
        "cliente_id": 99999,
        "placa": "FK001",
        "mecanico_id": mecanico_id
    }
    response = client.post("/orden/", json=datos, headers=auth_headers)
    assert response.status_code == 404
    assert "Cliente no encontrado" in response.json()["detail"]

def test_obtener_orden(client, auth_headers):
    cliente_datos = {
        "documento": "GETORD01",
        "nombre": "Cliente Obtener",
        "telefono": "3003334455",
        "correo": "get@orden.com",
        "direccion": "Calle Get"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "GETORD01")

    vehiculo_datos = {
        "placa": "GET001",
        "marca": "Kia",
        "modelo": "Rio",
        "ano": 2018,
        "color": "Gris",
        "kilometraje": 55000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECGET01",
        "nombre": "Mecánico Get",
        "especialidad": "Electricidad",
        "telefono": "3004445566",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECGET01")

    orden_datos = {
        "fecha": str(date.today()),
        "diagnostico": "Falla en el motor",
        "estado": "Pendiente",
        "observaciones": "Orden de prueba get",
        "costo_estimado": "150000",
        "cliente_id": cliente_id,
        "placa": "GET001",
        "mecanico_id": mecanico_id
    }
    crear = client.post("/orden/", json=orden_datos, headers=auth_headers)
    assert crear.status_code == 201
    orden_id = crear.json()["id"]

    response = client.get(f"/orden/{orden_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == orden_id
    assert response.json()["diagnostico"] == "Falla en el motor"

def test_obtener_orden_no_existente(client, auth_headers):
    response = client.get("/orden/99999", headers=auth_headers)
    assert response.status_code == 404
    assert "Orden no encontrada" in response.json()["detail"]

def test_listar_ordenes_por_estado(client, auth_headers):
    cliente_datos = {
        "documento": "ESTORD01",
        "nombre": "Cliente Estado",
        "telefono": "3005556677",
        "correo": "estado@orden.com",
        "direccion": "Calle Estado"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "ESTORD01")

    vehiculo_datos = {
        "placa": "EST001",
        "marca": "Hyundai",
        "modelo": "Accent",
        "ano": 2017,
        "color": "Negro",
        "kilometraje": 70000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECEST01",
        "nombre": "Mecánico Estado",
        "especialidad": "Suspensión",
        "telefono": "3006667788",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECEST01")

    orden_datos = {
        "fecha": str(date.today()),
        "diagnostico": "Revisión de frenos",
        "estado": "Pendiente",
        "observaciones": "Para filtrar por estado",
        "costo_estimado": "120000",
        "cliente_id": cliente_id,
        "placa": "EST001",
        "mecanico_id": mecanico_id
    }
    client.post("/orden/", json=orden_datos, headers=auth_headers)

    response = client.get("/orden/estado/Pendiente", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for orden in response.json():
        assert orden["estado"] == "Pendiente"

def test_actualizar_orden_completa(client, auth_headers):
    cliente_datos = {
        "documento": "PUTORD01",
        "nombre": "Cliente PUT",
        "telefono": "3007778899",
        "correo": "put@orden.com",
        "direccion": "Calle PUT"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "PUTORD01")

    vehiculo_datos = {
        "placa": "PUT001",
        "marca": "Ford",
        "modelo": "Fiesta",
        "ano": 2016,
        "color": "Verde",
        "kilometraje": 90000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECPUT01",
        "nombre": "Mecánico PUT",
        "especialidad": "Transmisión",
        "telefono": "3008889900",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECPUT01")

    orden_datos = {
        "fecha": str(date.today()),
        "diagnostico": "Original",
        "estado": "Pendiente",
        "observaciones": "Original",
        "costo_estimado": "100000",
        "cliente_id": cliente_id,
        "placa": "PUT001",
        "mecanico_id": mecanico_id
    }
    crear = client.post("/orden/", json=orden_datos, headers=auth_headers)
    orden_id = crear.json()["id"]

    datos_actualizar = {
        "fecha": str(date.today()),
        "diagnostico": "Diagnóstico actualizado completo",
        "estado": "En Proceso",
        "observaciones": "Actualizado por PUT",
        "costo_estimado": "250000.00",
        "cliente_id": cliente_id,
        "placa": "PUT001",
        "mecanico_id": mecanico_id
    }
    response = client.put(f"/orden/{orden_id}", json=datos_actualizar, headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["diagnostico"] == "Diagnóstico actualizado completo"
    assert response.json()["estado"] == "En Proceso"
    assert response.json()["observaciones"] == "Actualizado por PUT"

def test_actualizar_orden_parcial(client, auth_headers):
    cliente_datos = {
        "documento": "PATCHORD01",
        "nombre": "Cliente PATCH",
        "telefono": "3009990011",
        "correo": "patch@orden.com",
        "direccion": "Calle PATCH"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "PATCHORD01")

    vehiculo_datos = {
        "placa": "PATCH01",
        "marca": "Nissan",
        "modelo": "Versa",
        "ano": 2022,
        "color": "Blanco",
        "kilometraje": 15000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECPATCH01",
        "nombre": "Mecánico PATCH",
        "especialidad": "Diagnóstico",
        "telefono": "3000001122",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECPATCH01")

    orden_datos = {
        "fecha": str(date.today()),
        "diagnostico": "Falla en el motor",
        "estado": "Pendiente",
        "observaciones": "Original",
        "costo_estimado": "150000",
        "cliente_id": cliente_id,
        "placa": "PATCH01",
        "mecanico_id": mecanico_id
    }
    crear = client.post("/orden/", json=orden_datos, headers=auth_headers)
    orden_id = crear.json()["id"]

    response = client.patch(
        f"/orden/{orden_id}",
        json={
            "estado": "Completado",
            "observaciones": "Terminada por PATCH",
            "costo_estimado": "180000.75"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["estado"] == "Completado"
    assert response.json()["observaciones"] == "Terminada por PATCH"
    assert response.json()["diagnostico"] == "Falla en el motor"

def test_eliminar_orden(client, auth_headers):
    cliente_datos = {
        "documento": "DELORD01",
        "nombre": "Cliente Eliminar",
        "telefono": "3001112233",
        "correo": "del@orden.com",
        "direccion": "Calle Delete"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "DELORD01")

    vehiculo_datos = {
        "placa": "DEL001",
        "marca": "Renault",
        "modelo": "Sandero",
        "ano": 2015,
        "color": "Gris",
        "kilometraje": 110000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECDEL01",
        "nombre": "Mecánico Delete",
        "especialidad": "General",
        "telefono": "3002223344",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECDEL01")

    orden_datos = {
        "fecha": str(date.today()),
        "diagnostico": "Para eliminar",
        "estado": "Pendiente",
        "observaciones": "Se va a borrar",
        "costo_estimado": "50000",
        "cliente_id": cliente_id,
        "placa": "DEL001",
        "mecanico_id": mecanico_id
    }
    crear = client.post("/orden/", json=orden_datos, headers=auth_headers)
    orden_id = crear.json()["id"]

    response = client.delete(f"/orden/{orden_id}", headers=auth_headers)
    assert response.status_code == 204

    response_get = client.get(f"/orden/{orden_id}", headers=auth_headers)
    assert response_get.status_code == 404

def test_eliminar_orden_completada(client, auth_headers):
    cliente_datos = {
        "documento": "DELCOMP01",
        "nombre": "Cliente Completada",
        "telefono": "3003334455",
        "correo": "comp@orden.com",
        "direccion": "Calle Completada"
    }
    client.post("/cliente/", json=cliente_datos, headers=auth_headers)
    lista_clientes = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista_clientes.json() if c["documento"] == "DELCOMP01")

    vehiculo_datos = {
        "placa": "COMP01",
        "marca": "Volkswagen",
        "modelo": "Gol",
        "ano": 2014,
        "color": "Rojo",
        "kilometraje": 130000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=vehiculo_datos, headers=auth_headers)

    mecanico_datos = {
        "documento": "MECCOMP01",
        "nombre": "Mecánico Completada",
        "especialidad": "Motor",
        "telefono": "3004445566",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=mecanico_datos, headers=auth_headers)
    lista_mecanicos = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista_mecanicos.json() if m["documento"] == "MECCOMP01")