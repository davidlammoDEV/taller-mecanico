def test_listar_usuarios(client, auth_headers):
    response = client.get("/usuario/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_usuario(client, auth_headers):
    datos = {
        "iduser": "user01",
        "nombre": "Carlos",
        "apellido": "Pérez",
        "correo": "carlos.perez@test.com",
        "contrase": "clave123"
    }
    response = client.post("/usuario/", json=datos, headers=auth_headers)

    assert response.status_code in [200, 201]
    assert response.json()["iduser"] == "user01"
    assert response.json()["nombre"] == "Carlos"
    assert response.json()["apellido"] == "Pérez"
    assert response.json()["correo"] == "carlos.perez@test.com"

def test_crear_usuario_datos_invalidos(client, auth_headers):
    datos = {
        "nombre": "Sin iduser ni correo"
    }
    response = client.post("/usuario/", json=datos, headers=auth_headers)
    assert response.status_code == 422

def test_obtener_usuario(client, auth_headers):
    datos = {
        "iduser": "user02",
        "nombre": "Ana",
        "apellido": "García",
        "correo": "ana.garcia@test.com",
        "contrase": "clave456"
    }
    client.post("/usuario/", json=datos, headers=auth_headers)

    response = client.get("/usuario/user02", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["iduser"] == "user02"
    assert response.json()["nombre"] == "Ana"
    assert response.json()["apellido"] == "García"
    assert response.json()["correo"] == "ana.garcia@test.com"

def test_obtener_usuario_no_existente(client, auth_headers):
    response = client.get("/usuario/noexiste999", headers=auth_headers)
    assert response.status_code == 404

def test_actualizar_usuario_parcial(client, auth_headers):
    datos = {
        "iduser": "user03",
        "nombre": "Luis",
        "apellido": "Martínez",
        "correo": "luis.martinez@test.com",
        "contrase": "clave789"
    }
    client.post("/usuario/", json=datos, headers=auth_headers)

    response = client.patch(
        "/usuario/user03",
        json={
            "nombre": "Luis Actualizado",
            "apellido": "Martínez Gómez"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["nombre"] == "Luis Actualizado"
    assert response.json()["apellido"] == "Martínez Gómez"
    assert response.json()["iduser"] == "user03"
    assert response.json()["correo"] == "luis.martinez@test.com"

def test_eliminar_usuario(client, auth_headers):
    datos = {
        "iduser": "user04",
        "nombre": "Pedro",
        "apellido": "López",
        "correo": "pedro.lopez@test.com",
        "contrase": "clave000"
    }
    client.post("/usuario/", json=datos, headers=auth_headers)

    response = client.delete("/usuario/user04", headers=auth_headers)
    assert response.status_code == 204

    response_get = client.get("/usuario/user04", headers=auth_headers)
    assert response_get.status_code == 404

    lista_despues = client.get("/usuario/", headers=auth_headers)
    idusers = [u["iduser"] for u in lista_despues.json()]
    assert "user04" not in idusers