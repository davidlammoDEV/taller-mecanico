from models.rol_model import Rol

def test_listar_roles(client, auth_headers):
    response = client.get("/Rol/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_rol(client, auth_headers):
    datos = {
        "nombre": "Supervisor de Prueba",
        "descripcion": "Rol creado en test de pytest"
    }
    response = client.post("/Rol/", json=datos, headers=auth_headers)

    assert response.status_code in [200, 201]
    assert response.json()["nombre"] == "Supervisor de Prueba"
    assert response.json()["descripcion"] == "Rol creado en test de pytest"

def test_crear_rol_datos_invalidos(client, auth_headers):
    datos = {
        "nombre": "Solo nombre"
    }
    response = client.post("/Rol/", json=datos, headers=auth_headers)
    assert response.status_code == 422

def test_actualizar_rol_parcial(client, auth_headers, db_session):
    datos = {
        "nombre": "Rol Parcial",
        "descripcion": "Descripción original"
    }
    client.post("/Rol/", json=datos, headers=auth_headers)

    rol = db_session.query(Rol).filter(Rol.nombre == "Rol Parcial", Rol.activo == True).first()
    assert rol is not None
    idrol = rol.idrol

    response = client.patch(
        f"/Rol/{idrol}",
        json={
            "nombre": "Rol Actualizado",
            "descripcion": "Descripción actualizada por PATCH"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["nombre"] == "Rol Actualizado"
    assert response.json()["descripcion"] == "Descripción actualizada por PATCH"

def test_actualizar_rol_no_existente(client, auth_headers):
    response = client.patch(
        "/Rol/99999",
        json={"nombre": "No existe"},
        headers=auth_headers
    )
    assert response.status_code == 404

def test_eliminar_rol(client, auth_headers, db_session):
    datos = {
        "nombre": "Rol a Eliminar",
        "descripcion": "Este rol se va a borrar"
    }
    client.post("/Rol/", json=datos, headers=auth_headers)

    rol = db_session.query(Rol).filter(Rol.nombre == "Rol a Eliminar", Rol.activo == True).first()
    assert rol is not None
    idrol = rol.idrol

    response = client.delete(f"/Rol/{idrol}", headers=auth_headers)
    assert response.status_code == 204

    rol_despues = db_session.query(Rol).filter(Rol.idrol == idrol).first()
    assert rol_despues.activo == False


def test_eliminar_rol_no_existente(client, auth_headers):
    response = client.delete("/Rol/99999", headers=auth_headers)
    assert response.status_code == 404