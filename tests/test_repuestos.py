def test_listar_repuestos(client, auth_headers):
    response = client.get("/repuesto/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_repuesto(client, auth_headers):
    proveedor_datos = {
        "documento": "REP100200",
        "nombre": "Proveedor Repuesto",
        "nom_empresa": "Repuestos Test",
        "telefono": "3001112233",
        "correo": "repuesto@test.com"
    }
    client.post("/proveedor/", json=proveedor_datos, headers=auth_headers)
    lista_proveedores = client.get("/proveedor/", headers=auth_headers)
    proveedor_id = next(p["id"] for p in lista_proveedores.json() if p["documento"] == "REP100200")

    datos = {
        "codigo": "REP-001",
        "nombre": "Filtro de aceite",
        "marca": "Mann",
        "stock": 25,
        "costo": "15000",
        "precio": "28000",
        "descripcion": "Filtro de aceite original",
        "proveedor_id": proveedor_id
    }
    response = client.post("/repuesto/", json=datos, headers=auth_headers)

    assert response.status_code in [200, 201]
    assert response.json()["codigo"] == "REP-001"
    assert response.json()["nombre"] == "Filtro de aceite"
    assert response.json()["marca"] == "Mann"
    assert response.json()["stock"] == 25
    assert response.json()["proveedor_id"] == proveedor_id

def test_crear_repuesto_datos_invalidos(client, auth_headers):
    datos = {
        "nombre": "Sin código"
    }
    response = client.post("/repuesto/", json=datos, headers=auth_headers)
    assert response.status_code == 422

def test_obtener_repuesto(client, auth_headers):
    proveedor_datos = {
        "documento": "REP200300",
        "nombre": "Proveedor Get",
        "nom_empresa": "Get Parts",
        "telefono": "3002223344",
        "correo": "get@parts.com"
    }
    client.post("/proveedor/", json=proveedor_datos, headers=auth_headers)
    lista_proveedores = client.get("/proveedor/", headers=auth_headers)
    proveedor_id = next(p["id"] for p in lista_proveedores.json() if p["documento"] == "REP200300")

    datos = {
        "codigo": "REP-GET01",
        "nombre": "Pastillas de freno",
        "marca": "Bosch",
        "stock": 40,
        "costo": "35000",
        "precio": "65000",
        "descripcion": "Pastillas delanteras",
        "proveedor_id": proveedor_id
    }
    client.post("/repuesto/", json=datos, headers=auth_headers)

    response = client.get("/repuesto/REP-GET01", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["codigo"] == "REP-GET01"
    assert response.json()["nombre"] == "Pastillas de freno"
    assert response.json()["marca"] == "Bosch"

def test_obtener_repuesto_no_existente(client, auth_headers):
    response = client.get("/repuesto/NOEXISTE999", headers=auth_headers)
    assert response.status_code == 404

def test_actualizar_repuesto_completo(client, auth_headers):
    proveedor_datos = {
        "documento": "REP300400",
        "nombre": "Proveedor PUT",
        "nom_empresa": "PUT Parts",
        "telefono": "3003334455",
        "correo": "put@parts.com"
    }
    client.post("/proveedor/", json=proveedor_datos, headers=auth_headers)
    lista_proveedores = client.get("/proveedor/", headers=auth_headers)
    proveedor_id = next(p["id"] for p in lista_proveedores.json() if p["documento"] == "REP300400")

    datos = {
        "codigo": "REP-PUT01",
        "nombre": "Bujía original",
        "marca": "NGK",
        "stock": 50,
        "costo": "8000",
        "precio": "15000",
        "descripcion": "Bujía estándar",
        "proveedor_id": proveedor_id
    }
    client.post("/repuesto/", json=datos, headers=auth_headers)

    datos_actualizar = {
        "codigo": "REP-PUT01",
        "nombre": "Bujía iridium",
        "marca": "NGK",
        "stock": 60,
        "costo": "12000",
        "precio": "22000",
        "descripcion": "Bujía iridium actualizada",
        "proveedor_id": proveedor_id
    }
    response = client.put(
        "/repuesto/REP-PUT01",
        json=datos_actualizar,
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["nombre"] == "Bujía iridium"
    assert response.json()["stock"] == 60
    assert response.json()["descripcion"] == "Bujía iridium actualizada"

def test_actualizar_repuesto_parcial(client, auth_headers):
    proveedor_datos = {
        "documento": "REP400500",
        "nombre": "Proveedor PATCH",
        "nom_empresa": "PATCH Parts",
        "telefono": "3004445566",
        "correo": "patch@parts.com"
    }
    client.post("/proveedor/", json=proveedor_datos, headers=auth_headers)
    lista_proveedores = client.get("/proveedor/", headers=auth_headers)
    proveedor_id = next(p["id"] for p in lista_proveedores.json() if p["documento"] == "REP400500")

    datos = {
        "codigo": "REP-PATCH01",
        "nombre": "Aceite 5W30",
        "marca": "Mobil",
        "stock": 30,
        "costo": "25000",
        "precio": "45000",
        "descripcion": "Aceite sintético",
        "proveedor_id": proveedor_id
    }
    client.post("/repuesto/", json=datos, headers=auth_headers)

    response = client.patch(
        "/repuesto/REP-PATCH01",
        json={
            "stock": 45,
            "precio": "48000"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["stock"] == 45
    assert float(response.json()["precio"]) == 48000.0
    assert response.json()["nombre"] == "Aceite 5W30"
    assert response.json()["marca"] == "Mobil"

def test_eliminar_repuesto(client, auth_headers):
    proveedor_datos = {
        "documento": "REP500600",
        "nombre": "Proveedor Delete",
        "nom_empresa": "Delete Parts",
        "telefono": "3005556677",
        "correo": "delete@parts.com"
    }
    client.post("/proveedor/", json=proveedor_datos, headers=auth_headers)
    lista_proveedores = client.get("/proveedor/", headers=auth_headers)
    proveedor_id = next(p["id"] for p in lista_proveedores.json() if p["documento"] == "REP500600")

    datos = {
        "codigo": "REP-DEL01",
        "nombre": "Amortiguador",
        "marca": "Monroe",
        "stock": 10,
        "costo": "80000",
        "precio": "150000",
        "descripcion": "Amortiguador delantero",
        "proveedor_id": proveedor_id
    }
    client.post("/repuesto/", json=datos, headers=auth_headers)

    response = client.delete("/repuesto/REP-DEL01", headers=auth_headers)
    assert response.status_code == 204

    response_get = client.get("/repuesto/REP-DEL01", headers=auth_headers)
    assert response_get.status_code == 404

    lista_despues = client.get("/repuesto/", headers=auth_headers)
    codigos = [r["codigo"] for r in lista_despues.json()]
    assert "REP-DEL01" not in codigos