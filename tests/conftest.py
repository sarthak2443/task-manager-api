import os
import pytest
from app import create_app
from app.extensions import db

@pytest.fixture()
def app(tmp_path):
    os.environ["DATABASE_URL"] = f"sqlite:///{tmp_path/'test.db'}"
    os.environ["JWT_SECRET_KEY"] = "test-secret"
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def auth_headers(client):
    # register + login to get token
    client.post("/auth/register", json={"email": "u@example.com", "password": "secret12"})
    rv = client.post("/auth/login", json={"email": "u@example.com", "password": "secret12"})
    token = rv.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
