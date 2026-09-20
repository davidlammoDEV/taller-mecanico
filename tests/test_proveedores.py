def test_listar_proveedores(client, auth_headers):
    response = client.get("/proveedor/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_proveedor(client, auth_headers):
    datos = {
        "documento": "900100200",
        "nombre": "Carlos Proveedor",
        "nom_empresa": "Repuestos del Norte",
        "telefono": "3001112233",
        "correo": "carlos@repuestosnorte.com"
    }
    response = client.post("/proveedor/", json=datos, headers=auth_headers)

    assert response.status_code in [200, 201]
    assert response.json()["documento"] == "900100200"
    assert response.json()["nombre"] == "Carlos Proveedor"
    assert response.json()["nom_empresa"] == "Repuestos del Norte"

def test_crear_proveedor_datos_invalidos(client, auth_headers):
    datos = {
        "nombre": "Sin Documento"
    }
    response = client.post("/proveedor/", json=datos, headers=auth_headers)
    assert response.status_code == 422

def test_obtener_proveedor(client, auth_headers):
    datos = {
        "documento": "900200300",
        "nombre": "Ana Proveedora",
        "nom_empresa": "AutoPartes SA",
        "telefono": "3002223344",
        "correo": "ana@autopartes.com"
    }
    client.post("/proveedor/", json=datos, headers=auth_headers)

    lista = client.get("/proveedor/", headers=auth_headers)
    proveedor = next(p for p in lista.json() if p["documento"] == "900200300")
    proveedor_id = proveedor["id"]

    response = client.get(f"/proveedor/{proveedor_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["nombre"] == "Ana Proveedora"
    assert response.json()["nom_empresa"] == "AutoPartes SA"

def test_obtener_proveedor_no_existente(client, auth_headers):
    response = client.get("/proveedor/99999", headers=auth_headers)
    assert response.status_code == 404

def test_actualizar_proveedor_completo(client, auth_headers):
    datos = {
        "documento": "900300400",
        "nombre": "Pedro Original",
        "nom_empresa": "Original Parts",
        "telefono": "3003334455",
        "correo": "pedro@original.com"
    }
    client.post("/proveedor/", json=datos, headers=auth_headers)

    lista = client.get("/proveedor/", headers=auth_headers)
    proveedor_id = next(p["id"] for p in lista.json() if p["documento"] == "900300400")

    datos_actualizar = {
        "documento": "900300400",
        "nombre": "Pedro Actualizado",
        "nom_empresa": "Updated Parts",
        "telefono": "3009990011",
        "correo": "pedro@updated.com"
    }
    response = client.put(
        f"/proveedor/{proveedor_id}",
        json=datos_actualizar,
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["nombre"] == "Pedro Actualizado"
    assert response.json()["nom_empresa"] == "Updated Parts"
    assert response.json()["telefono"] == "3009990011"

def test_actualizar_proveedor_parcial(client, auth_headers):
    datos = {
        "documento": "900400500",
        "nombre": "Luis Parcial",
        "nom_empresa": "Parcial SA",
        "telefono": "3004445566",
        "correo": "luis@parcial.com"
    }
    client.post("/proveedor/", json=datos, headers=auth_headers)

    lista = client.get("/proveedor/", headers=auth_headers)
    proveedor_id = next(p["id"] for p in lista.json() if p["documento"] == "900400500")

    response = client.patch(
        f"/proveedor/{proveedor_id}",
        json={
            "nombre": "Luis Actualizado",
            "telefono": "3001110000"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["nombre"] == "Luis Actualizado"
    assert response.json()["telefono"] == "3001110000"
    assert response.json()["documento"] == "900400500"
    assert response.json()["nom_empresa"] == "Parcial SA"

def test_eliminar_proveedor(client, auth_headers):
    datos = {
        "documento": "900500600",
        "nombre": "Proveedor a Eliminar",
        "nom_empresa": "Eliminar Parts",
        "telefono": "3005556677",
        "correo": "eliminar@parts.com"
    }
    client.post("/proveedor/", json=datos, headers=auth_headers)

    lista = client.get("/proveedor/", headers=auth_headers)
    proveedor_id = next(p["id"] for p in lista.json() if p["documento"] == "900500600")

    response = client.delete(f"/proveedor/{proveedor_id}", headers=auth_headers)
    assert response.status_code == 204

    response_get = client.get(f"/proveedor/{proveedor_id}", headers=auth_headers)
    assert response_get.status_code == 404

    lista_despues = client.get("/proveedor/", headers=auth_headers)
    documentos = [p["documento"] for p in lista_despues.json()]
    assert "900500600" not in documentos