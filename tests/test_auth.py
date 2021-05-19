import atexit
import json

from authentication.models import RegisterModel
from authentication.utils import ALGORITHM, SECRET_KEY
from fastapi.testclient import TestClient
from jose import jwt, jws
from main import app
from orm import User, create_tables, drop_tables

create_tables()
atexit.register(drop_tables)

client = TestClient(app)

user_model = RegisterModel(
    full_name="Test User",
    email="test@mail.local",
    phone="88000000000",
    password="password",
)


def test_register():
    response = client.post(
        "/auth/register",
        user_model.json(),
    )
    assert response.status_code == 200

    data = json.loads(response.content)
    assert data["full_name"] == user_model.full_name
    assert data["email"] == user_model.email
    assert data["phone"] == user_model.phone

    user = User.get_by_id(1)
    user.is_active = True
    user.save()


def test_token():
    response = client.post("/auth/token", user_model.json())
    assert response.status_code == 200

    token = json.loads(response.content).get("access_token")
    assert jws.verify(token, SECRET_KEY, ALGORITHM)

    decode_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
    assert decode_token["email"] == user_model.email


def test_login():
    response = client.post("/auth/login", user_model.json())
    assert response.status_code == 200

    token = response.headers.get("authorization").split()[-1]
    assert jws.verify(token, SECRET_KEY, ALGORITHM)
