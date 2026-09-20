from datetime import date

def test_listar_mecanicos(client, auth_headers):
    response = client.get("/mecanico/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_mecanico(client, auth_headers):
    datos = {
        "documento": "100200300",
        "nombre": "Carlos Mecánico",
        "especialidad": "Motor",
        "telefono": "3001112233",
        "fecha_ingreso": str(date.today())
    }
    response = client.post("/mecanico/", json=datos, headers=auth_headers)

    assert response.status_code in [200, 201]
    assert response.json()["documento"] == "100200300"
    assert response.json()["nombre"] == "Carlos Mecánico"

def test_crear_mecanico_datos_invalidos(client, auth_headers):
    datos = {
        "nombre": "Sin Documento"
    }
    response = client.post("/mecanico/", json=datos, headers=auth_headers)
    assert response.status_code == 422

def test_crear_mecanico_documento_duplicado(client, auth_headers):
    datos = {
        "documento": "555666777",
        "nombre": "Mecánico Original",
        "especialidad": "Frenos",
        "telefono": "3005556677",
        "fecha_ingreso": str(date.today())
    }

    response1 = client.post("/mecanico/", json=datos, headers=auth_headers)
    assert response1.status_code in [200, 201]

    response2 = client.post("/mecanico/", json=datos, headers=auth_headers)
    assert response2.status_code == 409


def test_obtener_mecanico(client, auth_headers):
    datos = {
        "documento": "888999000",
        "nombre": "Ana Mecánica",
        "especialidad": "Electricidad",
        "telefono": "3008889900",
        "fecha_ingreso": str(date.today())
    }
    crear = client.post("/mecanico/", json=datos, headers=auth_headers)
    assert crear.status_code in [200, 201]

    lista = client.get("/mecanico/", headers=auth_headers)
    mecanico = next(m for m in lista.json() if m["documento"] == "888999000")
    mecanico_id = mecanico["id"]

    response = client.get(f"/mecanico/{mecanico_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["nombre"] == "Ana Mecánica"

def test_obtener_mecanico_no_existente(client, auth_headers):
    response = client.get("/mecanico/99999", headers=auth_headers)
    assert response.status_code == 404

def test_actualizar_mecanico_completo(client, auth_headers):
    datos = {
        "documento": "111222333",
        "nombre": "Pedro Original",
        "especialidad": "Suspensión",
        "telefono": "3001112222",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=datos, headers=auth_headers)

    lista = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista.json() if m["documento"] == "111222333")

    datos_actualizar = {
        "documento": "111222333",
        "nombre": "Pedro Actualizado",
        "especialidad": "Transmisión",
        "telefono": "3009998888",
        "fecha_ingreso": str(date.today())
    }
    response = client.put(f"/mecanico/{mecanico_id}", json=datos_actualizar, headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["nombre"] == "Pedro Actualizado"
    assert response.json()["especialidad"] == "Transmisión"

def test_actualizar_mecanico_parcial(client, auth_headers):
    datos = {
        "documento": "444555666",
        "nombre": "Luis Parcial",
        "especialidad": "General",
        "telefono": "3004445555",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=datos, headers=auth_headers)

    lista = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista.json() if m["documento"] == "444555666")

    response = client.patch(
        f"/mecanico/{mecanico_id}",
        json={"especialidad": "Diagnóstico", "telefono": "3007776666"},
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["especialidad"] == "Diagnóstico"
    assert response.json()["telefono"] == "3007776666"
    assert response.json()["nombre"] == "Luis Parcial"

def test_eliminar_mecanico(client, auth_headers):
    datos = {
        "documento": "777888999",
        "nombre": "Mecánico a Eliminar",
        "especialidad": "Pintura",
        "telefono": "3007778888",
        "fecha_ingreso": str(date.today())
    }
    client.post("/mecanico/", json=datos, headers=auth_headers)

    lista = client.get("/mecanico/", headers=auth_headers)
    mecanico_id = next(m["id"] for m in lista.json() if m["documento"] == "777888999")

    response = client.delete(f"/mecanico/{mecanico_id}", headers=auth_headers)
    assert response.status_code == 204

    response_get = client.get(f"/mecanico/{mecanico_id}", headers=auth_headers)
    assert response_get.status_code == 404

    lista_despues = client.get("/mecanico/", headers=auth_headers)
    documentos = [m["documento"] for m in lista_despues.json()]
    assert "777888999" not in documentos