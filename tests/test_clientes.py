def test_listar_clientes(client, auth_headers):
    response = client.get("/cliente/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_cliente(client, auth_headers):
    datos = {
        "documento": "123456789",
        "nombre": "Juan Pérez",
        "telefono": "3001234567",
        "correo": "juan@example.com",
        "direccion": "Calle 10 #20-30"
    }
    response = client.post("/cliente/", json=datos, headers=auth_headers)

    assert response.status_code in [200, 201]
    assert response.json()["documento"] == "123456789"
    assert response.json()["nombre"] == "Juan Pérez"

def test_crear_cliente_datos_invalidos(client, auth_headers):
    datos = {
        "nombre": "Sin Documento"
    }
    response = client.post("/cliente/", json=datos, headers=auth_headers)
    assert response.status_code == 422


def test_crear_cliente_documento_duplicado(client, auth_headers):
    datos = {
        "documento": "111222333",
        "nombre": "Cliente Original",
        "telefono": "3001112233",
        "correo": "original@example.com",
        "direccion": "Calle Original"
    }

    response1 = client.post("/cliente/", json=datos, headers=auth_headers)
    assert response1.status_code in [200, 201]

    response2 = client.post("/cliente/", json=datos, headers=auth_headers)
    assert response2.status_code == 409

def test_obtener_cliente_no_existente(client, auth_headers):
    """Debe devolver 404 cuando el cliente no existe"""
    response = client.get("/cliente/99999", headers=auth_headers)
    assert response.status_code == 404

def test_actualizar_cliente_completo(client, auth_headers):
    datos_crear = {
        "documento": "444555666",
        "nombre": "Cliente Actualizar",
        "telefono": "3004445566",
        "correo": "actualizar@example.com",
        "direccion": "Dirección vieja"
    }
    crear = client.post("/cliente/", json=datos_crear, headers=auth_headers)
    assert crear.status_code in [200, 201]

    cliente_id = crear.json().get("id")

    if not cliente_id:
        lista = client.get("/cliente/", headers=auth_headers)
        cliente_id = next(c["id"] for c in lista.json() if c["documento"] == "444555666")

    datos_actualizar = {
        "documento": "444555666",
        "nombre": "Cliente Actualizado",
        "telefono": "3009998877",
        "correo": "actualizado@example.com",
        "direccion": "Nueva dirección"
    }
    response = client.put(f"/cliente/{cliente_id}", json=datos_actualizar, headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["nombre"] == "Cliente Actualizado"
    assert response.json()["telefono"] == "3009998877"


def test_actualizar_cliente_parcial(client, auth_headers):
    datos = {
        "documento": "777888999",
        "nombre": "Cliente Parcial",
        "direccion": "Dirección parcial"
    }
    crear = client.post("/cliente/", json=datos, headers=auth_headers)
    assert crear.status_code in [200, 201]

    lista = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista.json() if c["documento"] == "777888999")

    response = client.patch(
        f"/cliente/{cliente_id}",
        json={"nombre": "Nombre Parcialmente Actualizado"},
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["nombre"] == "Nombre Parcialmente Actualizado"
    assert response.json()["documento"] == "777888999"

def test_eliminar_cliente(client, auth_headers):
    datos = {
        "documento": "000111222",
        "nombre": "Cliente a Eliminar",
        "direccion": "Por eliminar"
    }
    crear = client.post("/cliente/", json=datos, headers=auth_headers)
    assert crear.status_code in [200, 201]

    lista = client.get("/cliente/", headers=auth_headers)
    cliente_id = next(c["id"] for c in lista.json() if c["documento"] == "000111222")

    response = client.delete(f"/cliente/{cliente_id}", headers=auth_headers)
    assert response.status_code == 204

    lista_despues = client.get("/cliente/", headers=auth_headers)
    documentos = [c["documento"] for c in lista_despues.json()]
    assert "000111222" not in documentos

    response_get = client.get(f"/cliente/{cliente_id}", headers=auth_headers)
    assert response_get.status_code == 404