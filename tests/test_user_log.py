from models.user_login_model import User_Log
from models.rol_model import Rol

def test_listar_usuarios_rol(client, auth_headers):
    response = client.get("/usuarios-roles/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_crear_usuario_rol(client, auth_headers, db_session):
    rol = db_session.query(Rol).filter(Rol.idrol == 2).first()
    if not rol:
        rol = Rol(idrol=2, nombre="Administrador", descripcion="Admin")
        db_session.add(rol)
        db_session.commit()

    usuario_datos = {
        "iduser": "ulog01",
        "nombre": "Usuario",
        "apellido": "Log",
        "correo": "ulog01@test.com",
        "contrase": "clave123"
    }
    client.post("/usuario/", json=usuario_datos, headers=auth_headers)

    datos = {
        "iduser": "ulog01",
        "idrol": 2
    }
    response = client.post("/usuarios-roles/", json=datos, headers=auth_headers)

    assert response.status_code in [200, 201]
    assert response.json()["iduser"] == "ulog01"
    assert response.json()["idrol"] == 2

def test_crear_usuario_rol_datos_invalidos(client, auth_headers):
    datos = {
        "iduser": "solo_user"
    }
    response = client.post("/usuarios-roles/", json=datos, headers=auth_headers)
    assert response.status_code == 422

def test_crear_usuario_rol_usuario_no_existente(client, auth_headers):
    datos = {
        "iduser": "noexiste999",
        "idrol": 2
    }
    response = client.post("/usuarios-roles/", json=datos, headers=auth_headers)
    assert response.status_code == 404
    assert "no existe" in response.json()["detail"].lower()

def test_crear_usuario_rol_rol_no_existente(client, auth_headers):
    usuario_datos = {
        "iduser": "ulog02",
        "nombre": "Sin",
        "apellido": "Rol",
        "correo": "ulog02@test.com",
        "contrase": "clave456"
    }
    client.post("/usuario/", json=usuario_datos, headers=auth_headers)

    datos = {
        "iduser": "ulog02",
        "idrol": 99999
    }
    response = client.post("/usuarios-roles/", json=datos, headers=auth_headers)
    assert response.status_code == 404
    assert "rol" in response.json()["detail"].lower()

def test_actualizar_usuario_rol_parcial(client, auth_headers, db_session):
    for idrol, nombre in [(2, "Administrador"), (3, "Mecanico")]:
        rol = db_session.query(Rol).filter(Rol.idrol == idrol).first()
        if not rol:
            db_session.add(Rol(idrol=idrol, nombre=nombre, descripcion=nombre))
    db_session.commit()

    usuario_datos = {
        "iduser": "ulog03",
        "nombre": "Patch",
        "apellido": "UserLog",
        "correo": "ulog03@test.com",
        "contrase": "clave789"
    }
    client.post("/usuario/", json=usuario_datos, headers=auth_headers)

    client.post(
        "/usuarios-roles/",
        json={"iduser": "ulog03", "idrol": 2},
        headers=auth_headers
    )

    registro = db_session.query(User_Log).filter(
        User_Log.iduser == "ulog03",
        User_Log.activo == True
    ).first()
    assert registro is not None
    iduser_log = getattr(registro, "idsuer_log", None) or getattr(registro, "iduser_log", None)

    response = client.patch(
        f"/usuarios-roles/{iduser_log}",
        json={"idrol": 3},
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["idrol"] == 3
    assert response.json()["iduser"] == "ulog03"

def test_actualizar_usuario_rol_no_existente(client, auth_headers):
    response = client.patch(
        "/usuarios-roles/99999",
        json={"idrol": 2},
        headers=auth_headers
    )
    assert response.status_code == 404

def test_eliminar_usuario_rol(client, auth_headers, db_session):
    rol = db_session.query(Rol).filter(Rol.idrol == 2).first()
    if not rol:
        db_session.add(Rol(idrol=2, nombre="Administrador", descripcion="Admin"))
        db_session.commit()

    usuario_datos = {
        "iduser": "ulog04",
        "nombre": "Delete",
        "apellido": "UserLog",
        "correo": "ulog04@test.com",
        "contrase": "clave000"
    }
    client.post("/usuario/", json=usuario_datos, headers=auth_headers)

    client.post(
        "/usuarios-roles/",
        json={"iduser": "ulog04", "idrol": 2},
        headers=auth_headers
    )

    registro = db_session.query(User_Log).filter(
        User_Log.iduser == "ulog04",
        User_Log.activo == True
    ).first()
    assert registro is not None
    iduser_log = getattr(registro, "idsuer_log", None) or getattr(registro, "iduser_log", None)

    response = client.delete(f"/usuarios-roles/{iduser_log}", headers=auth_headers)
    assert response.status_code == 204

    db_session.expire_all()
    registro_despues = db_session.query(User_Log).filter(
        User_Log.iduser == "ulog04"
    ).first()
    assert registro_despues.activo == False

def test_eliminar_usuario_rol_no_existente(client, auth_headers):
    response = client.delete("/usuarios-roles/99999", headers=auth_headers)
    assert response.status_code == 404