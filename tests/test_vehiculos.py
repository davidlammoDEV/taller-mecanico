def crear_cliente_de_prueba(client, auth_headers):
    datos = {
        "documento": "999888777",
        "nombre": "Cliente Dueño del Vehículo",
        "telefono": "3009998877",
        "correo": "dueno@example.com",
        "direccion": "Calle del Vehículo"
    }
    response = client.post("/cliente/", json=datos, headers=auth_headers)
    assert response.status_code in [200, 201]

    lista = client.get("/cliente/", headers=auth_headers)
    cliente = next(c for c in lista.json() if c["documento"] == "999888777")
    return cliente["id"]

def test_listar_vehiculos(client, auth_headers):
    response = client.get("/vehiculo/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_vehiculo(client, auth_headers):
    cliente_id = crear_cliente_de_prueba(client, auth_headers)

    datos = {
        "placa": "ABC123",
        "marca": "Toyota",
        "modelo": "Corolla",
        "ano": 2020,
        "color": "Blanco",
        "kilometraje": 45000,
        "observaciones": "Vehículo de prueba",
        "cliente_id": cliente_id
    }
    response = client.post("/vehiculo/", json=datos, headers=auth_headers)

    assert response.status_code in [200, 201]
    assert response.json()["placa"] == "ABC123"
    assert response.json()["marca"] == "Toyota"
    assert response.json()["cliente_id"] == cliente_id

def test_crear_vehiculo_datos_invalidos(client, auth_headers):
    """Debe fallar con 422 por datos incompletos"""
    datos = {
        "placa": "XYZ999",
        "marca": "Mazda"
    }
    response = client.post("/vehiculo/", json=datos, headers=auth_headers)
    assert response.status_code == 422

def test_obtener_vehiculo(client, auth_headers):
    cliente_id = crear_cliente_de_prueba(client, auth_headers)

    datos = {
        "placa": "DEF456",
        "marca": "Chevrolet",
        "modelo": "Spark",
        "ano": 2018,
        "color": "Rojo",
        "kilometraje": 60000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=datos, headers=auth_headers)

    response = client.get("/vehiculo/DEF456", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["placa"] == "DEF456"
    assert response.json()["marca"] == "Chevrolet"

def test_obtener_vehiculo_no_existente(client, auth_headers):
    response = client.get("/vehiculo/NOEXISTE", headers=auth_headers)
    assert response.status_code == 404

def test_actualizar_vehiculo_completo(client, auth_headers):
    cliente_id = crear_cliente_de_prueba(client, auth_headers)

    datos_crear = {
        "placa": "GHI789",
        "marca": "Kia",
        "modelo": "Rio",
        "ano": 2019,
        "color": "Gris",
        "kilometraje": 30000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=datos_crear, headers=auth_headers)

    datos_actualizar = {
        "placa": "GHI789",
        "marca": "Kia",
        "modelo": "Rio Actualizado",
        "ano": 2021,
        "color": "Negro",
        "kilometraje": 35000,
        "observaciones": "Actualizado en test",
        "cliente_id": cliente_id
    }
    response = client.put("/vehiculo/GHI789", json=datos_actualizar, headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["modelo"] == "Rio Actualizado"
    assert response.json()["color"] == "Negro"
    assert response.json()["ano"] == 2021

def test_actualizar_vehiculo_parcial(client, auth_headers):
    cliente_id = crear_cliente_de_prueba(client, auth_headers)

    datos = {
        "placa": "JKL012",
        "marca": "Hyundai",
        "modelo": "Accent",
        "ano": 2017,
        "color": "Azul",
        "kilometraje": 80000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=datos, headers=auth_headers)

    response = client.patch(
        "/vehiculo/JKL012",
        json={
            "color": "Plateado",
            "kilometraje": 82000
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["color"] == "Plateado"
    assert response.json()["kilometraje"] == 82000
    assert response.json()["marca"] == "Hyundai"

def test_eliminar_vehiculo(client, auth_headers):
    cliente_id = crear_cliente_de_prueba(client, auth_headers)

    datos = {
        "placa": "MNO345",
        "marca": "Ford",
        "modelo": "Fiesta",
        "ano": 2016,
        "color": "Verde",
        "kilometraje": 95000,
        "cliente_id": cliente_id
    }
    client.post("/vehiculo/", json=datos, headers=auth_headers)

    response = client.delete("/vehiculo/MNO345", headers=auth_headers)
    assert response.status_code == 204

    response_get = client.get("/vehiculo/MNO345", headers=auth_headers)
    assert response_get.status_code == 404

    lista = client.get("/vehiculo/", headers=auth_headers)
    placas = [v["placa"] for v in lista.json()]
    assert "MNO345" not in placas