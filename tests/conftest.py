import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database.connection import get_db
from models.base import Base

from models.usuario_model import Usuario
from models.user_login_model import User_Log
from models.rol_model import Rol
from tokensitos.tokensificador import hashear_password

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:3690@localhost:5432/taller_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()

@pytest.fixture
def token(client, db_session):
    rol = db_session.query(Rol).filter(Rol.idrol == 2).first()
    if not rol:
        rol = Rol(
            idrol=2,
            nombre="Administrador",
            descripcion="Rol de administrador del sistema"
        )
        db_session.add(rol)
        db_session.commit()

    usuario = Usuario(
        iduser="test01",
        nombre="Usuario",
        apellido="Prueba",
        contrase=hashear_password("123456"),
        correo="test@example.com"
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)

    user_log = User_Log(
        iduser=usuario.iduser,
        idrol=2,
        activo=True
    )
    db_session.add(user_log)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200, f"Error en login: {response.json()}"
    return response.json()["access_token"]

@pytest.fixture
def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}