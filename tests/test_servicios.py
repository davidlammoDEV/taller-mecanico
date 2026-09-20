def test_listar_servicios(client, auth_headers):
    response = client.get("/servicio/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_servicio(client, auth_headers):
    datos = {
        "nombre": "Cambio de aceite",
        "costo_base": "45000",
        "descripcion": "Cambio de aceite y filtro"
    }
    response = client.post("/servicio/", json=datos, headers=auth_headers)

    assert response.status_code in [200, 201]
    assert response.json()["nombre"] == "Cambio de aceite"
    assert response.json()["descripcion"] == "Cambio de aceite y filtro"

def test_crear_servicio_datos_invalidos(client, auth_headers):
    datos = {
        "nombre": "Sin costo"
    }
    response = client.post("/servicio/", json=datos, headers=auth_headers)
    assert response.status_code == 422

def test_obtener_servicio(client, auth_headers):
    datos = {
        "nombre": "Alineación y balanceo",
        "costo_base": "80000",
        "descripcion": "Alineación y balanceo de llantas"
    }
    client.post("/servicio/", json=datos, headers=auth_headers)

    lista = client.get("/servicio/", headers=auth_headers)
    servicio = next(s for s in lista.json() if s["nombre"] == "Alineación y balanceo")
    servicio_id = servicio["id"]

    response = client.get(f"/servicio/{servicio_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["nombre"] == "Alineación y balanceo"
    assert response.json()["descripcion"] == "Alineación y balanceo de llantas"

def test_obtener_servicio_no_existente(client, auth_headers):
    response = client.get("/servicio/99999", headers=auth_headers)
    assert response.status_code == 404

def test_actualizar_servicio_completo(client, auth_headers):
    datos = {
        "nombre": "Revisión de frenos",
        "costo_base": "60000",
        "descripcion": "Revisión original"
    }
    client.post("/servicio/", json=datos, headers=auth_headers)

    lista = client.get("/servicio/", headers=auth_headers)
    servicio_id = next(s["id"] for s in lista.json() if s["nombre"] == "Revisión de frenos")

    datos_actualizar = {
        "nombre": "Revisión de frenos completa",
        "costo_base": "75000",
        "descripcion": "Revisión y cambio de pastillas"
    }
    response = client.put(
        f"/servicio/{servicio_id}",
        json=datos_actualizar,
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["nombre"] == "Revisión de frenos completa"
    assert float(response.json()["costo_base"]) == 75000.0
    assert response.json()["descripcion"] == "Revisión y cambio de pastillas"

def test_actualizar_servicio_parcial(client, auth_headers):
    datos = {
        "nombre": "Diagnóstico electrónico",
        "costo_base": "50000",
        "descripcion": "Diagnóstico original"
    }
    client.post("/servicio/", json=datos, headers=auth_headers)

    lista = client.get("/servicio/", headers=auth_headers)
    servicio_id = next(s["id"] for s in lista.json() if s["nombre"] == "Diagnóstico electrónico")

    response = client.patch(
        f"/servicio/{servicio_id}",
        json={
            "costo_base": "55000",
            "descripcion": "Diagnóstico actualizado por PATCH"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert float(response.json()["costo_base"]) == 55000.0
    assert response.json()["descripcion"] == "Diagnóstico actualizado por PATCH"
    assert response.json()["nombre"] == "Diagnóstico electrónico"

def test_eliminar_servicio(client, auth_headers):
    datos = {
        "nombre": "Servicio a Eliminar",
        "costo_base": "30000",
        "descripcion": "Este servicio se va a borrar"
    }
    client.post("/servicio/", json=datos, headers=auth_headers)

    lista = client.get("/servicio/", headers=auth_headers)
    servicio_id = next(s["id"] for s in lista.json() if s["nombre"] == "Servicio a Eliminar")

    response = client.delete(f"/servicio/{servicio_id}", headers=auth_headers)
    assert response.status_code == 204

    response_get = client.get(f"/servicio/{servicio_id}", headers=auth_headers)
    assert response_get.status_code == 404

    lista_despues = client.get("/servicio/", headers=auth_headers)
    nombres = [s["nombre"] for s in lista_despues.json()]
    assert "Servicio a Eliminar" not in nombres