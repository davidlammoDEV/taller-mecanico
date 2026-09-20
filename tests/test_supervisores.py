from datetime import date

def test_listar_supervisores(client, auth_headers):
    response = client.get("/supervisor/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_supervisor(client, auth_headers):
    datos = {
        "documento": "200300400",
        "nombre": "Laura Supervisora",
        "telefono": "3002223344",
        "fecha_ingreso": str(date.today())
    }
    response = client.post("/supervisor/", json=datos, headers=auth_headers)

    assert response.status_code in [200, 201]
    assert response.json()["documento"] == "200300400"
    assert response.json()["nombre"] == "Laura Supervisora"

def test_crear_supervisor_datos_invalidos(client, auth_headers):

    datos = {
        "nombre": "Sin Documento"
    }
    response = client.post("/supervisor/", json=datos, headers=auth_headers)
    assert response.status_code == 422

def test_crear_supervisor_documento_duplicado(client, auth_headers):
    datos = {
        "documento": "300400500",
        "nombre": "Supervisor Original",
        "telefono": "3003334455",
        "fecha_ingreso": str(date.today())
    }

    response1 = client.post("/supervisor/", json=datos, headers=auth_headers)
    assert response1.status_code in [200, 201]

    response2 = client.post("/supervisor/", json=datos, headers=auth_headers)
    assert response2.status_code == 409

def test_obtener_supervisor(client, auth_headers):
    datos = {
        "documento": "400500600",
        "nombre": "Miguel Supervisor",
        "telefono": "3004445566",
        "fecha_ingreso": str(date.today())
    }
    client.post("/supervisor/", json=datos, headers=auth_headers)

    lista = client.get("/supervisor/", headers=auth_headers)
    supervisor = next(s for s in lista.json() if s["documento"] == "400500600")
    supervisor_id = supervisor["id"]

    response = client.get(f"/supervisor/{supervisor_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["nombre"] == "Miguel Supervisor"

def test_obtener_supervisor_no_existente(client, auth_headers):
    response = client.get("/supervisor/99999", headers=auth_headers)
    assert response.status_code == 404

def test_actualizar_supervisor_completo(client, auth_headers):
    datos = {
        "documento": "500600700",
        "nombre": "Sofia Original",
        "telefono": "3005556677",
        "fecha_ingreso": str(date.today())
    }
    client.post("/supervisor/", json=datos, headers=auth_headers)

    lista = client.get("/supervisor/", headers=auth_headers)
    supervisor_id = next(s["id"] for s in lista.json() if s["documento"] == "500600700")

    datos_actualizar = {
        "documento": "500600700",
        "nombre": "Sofia Actualizada",
        "telefono": "3009990011",
        "fecha_ingreso": str(date.today())
    }
    response = client.put(
        f"/supervisor/{supervisor_id}",
        json=datos_actualizar,
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["nombre"] == "Sofia Actualizada"
    assert response.json()["telefono"] == "3009990011"

def test_actualizar_supervisor_parcial(client, auth_headers):
    datos = {
        "documento": "600700800",
        "nombre": "Andres Parcial",
        "telefono": "3006667788",
        "fecha_ingreso": str(date.today())
    }
    client.post("/supervisor/", json=datos, headers=auth_headers)

    lista = client.get("/supervisor/", headers=auth_headers)
    supervisor_id = next(s["id"] for s in lista.json() if s["documento"] == "600700800")

    response = client.patch(
        f"/supervisor/{supervisor_id}",
        json={"nombre": "Andres Actualizado", "telefono": "3001110000"},
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["nombre"] == "Andres Actualizado"
    assert response.json()["telefono"] == "3001110000"
    assert response.json()["documento"] == "600700800"

def test_eliminar_supervisor(client, auth_headers):
    datos = {
        "documento": "700800900",
        "nombre": "Supervisor a Eliminar",
        "telefono": "3007778899",
        "fecha_ingreso": str(date.today())
    }
    client.post("/supervisor/", json=datos, headers=auth_headers)

    lista = client.get("/supervisor/", headers=auth_headers)
    supervisor_id = next(s["id"] for s in lista.json() if s["documento"] == "700800900")

    response = client.delete(f"/supervisor/{supervisor_id}", headers=auth_headers)
    assert response.status_code == 204

    response_get = client.get(f"/supervisor/{supervisor_id}", headers=auth_headers)
    assert response_get.status_code == 404

    lista_despues = client.get("/supervisor/", headers=auth_headers)
    documentos = [s["documento"] for s in lista_despues.json()]
    assert "700800900" not in documentos