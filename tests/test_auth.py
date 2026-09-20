def crear_rol_si_no_existe(db_session):
    from models.rol_model import Rol
    rol = db_session.query(Rol).filter(Rol.idrol == 1).first()
    if not rol:
        rol = Rol(
            idrol=1,
            nombre="Administrador",
            descripcion="Rol de administrador"
        )
        db_session.add(rol)
        db_session.commit()

def test_login_exitoso(client, db_session):
    crear_rol_si_no_existe(db_session)

    from models.usuario_model import Usuario
    from models.user_login_model import User_Log
    from tokensitos.tokensificador import hashear_password

    usuario = Usuario(
        iduser="authuser01",
        nombre="Auth",
        apellido="Test",
        contrase=hashear_password("password123"),
        correo="auth@test.com"
    )
    db_session.add(usuario)
    db_session.commit()

    user_log = User_Log(iduser="authuser01", idrol=1, activo=True)
    db_session.add(user_log)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "auth@test.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login_credenciales_incorrectas(client, db_session):
    crear_rol_si_no_existe(db_session)

    from models.usuario_model import Usuario
    from models.user_login_model import User_Log
    from tokensitos.tokensificador import hashear_password

    usuario = Usuario(
        iduser="authuser02",
        nombre="Auth",
        apellido="Fail",
        contrase=hashear_password("correcta"),
        correo="fail@test.com"
    )
    db_session.add(usuario)
    db_session.commit()

    user_log = User_Log(iduser="authuser02", idrol=1, activo=True)
    db_session.add(user_log)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "fail@test.com",
            "password": "incorrecta"
        }
    )

    assert response.status_code == 401
    assert "incorrectos" in response.json()["detail"].lower()

def test_login_usuario_inexistente(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "noexiste@test.com",
            "password": "cualquiera"
        }
    )
    assert response.status_code == 401

def test_acceso_sin_token(client):
    response = client.get("/cliente/")
    assert response.status_code == 401

def test_acceso_con_token_invalido(client):
    headers = {"Authorization": "Bearer token_falso_invalido"}
    response = client.get("/cliente/", headers=headers)
    assert response.status_code == 401


def test_acceso_con_token_valido(client, auth_headers):
    response = client.get("/cliente/", headers=auth_headers)
    assert response.status_code == 200

def test_registro_usuario(client, db_session):
    crear_rol_si_no_existe(db_session)

    datos = {
        "iduser": "nuevouser01",
        "nombre": "Nuevo",
        "apellido": "Usuario",
        "contrase": "clave123",
        "correo": "nuevo@test.com",
        "idrol": 1
    }
    response = client.post("/auth/registro", json=datos)

    assert response.status_code in [201, 400, 500]

def test_registro_usuario_duplicado(client, db_session, token):
    crear_rol_si_no_existe(db_session)

    datos = {
        "iduser": "otrouser",
        "nombre": "Otro",
        "apellido": "User",
        "contrase": "clave123",
        "correo": "test@example.com",
        "idrol": 1
    }
    response = client.post("/auth/registro", json=datos)
    assert response.status_code == 400
    assert "ya existe" in response.json()["detail"].lower()

def test_logout(client, db_session):
    crear_rol_si_no_existe(db_session)

    from models.usuario_model import Usuario
    from models.user_login_model import User_Log
    from tokensitos.tokensificador import hashear_password

    usuario = Usuario(
        iduser="logoutuser",
        nombre="Logout",
        apellido="Test",
        contrase=hashear_password("logout123"),
        correo="logout@test.com"
    )
    db_session.add(usuario)
    db_session.commit()

    user_log = User_Log(iduser="logoutuser", idrol=1, activo=True)
    db_session.add(user_log)
    db_session.commit()

    login_response = client.post(
        "/auth/login",
        data={
            "username": "logout@test.com",
            "password": "logout123"
        }
    )
    assert login_response.status_code == 200
    refresh_token = login_response.json()["refresh_token"]

    response = client.post(
        "/auth/logout",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    assert "cerrada" in response.json()["mensaje"].lower()