
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    # Create an isolated, in-memory SQLite database.
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )

    # Create the tables in the test database only.
    Base.metadata.create_all(bind=test_engine)

    def override_get_db() -> Generator[Session, None, None]:
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=test_engine)
        test_engine.dispose()



TEST_USER = {
    "email": "auth-test@example.com",
    "password": "StrongTestPassword123!",
    "display_name": "Auth Test User",
}


def register_test_user(client: TestClient) -> None:
    response = client.post("/auth/register", json=TEST_USER)
    assert response.status_code == 201, (
        f"Registration failed: {response.status_code} "
        f"- {response.text}"
    )


def test_register_user(client: TestClient):
    response = client.post("/auth/register", json=TEST_USER)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == TEST_USER["email"]
    assert data["display_name"] == TEST_USER["display_name"]
    assert "password_hash" not in data


def test_reject_duplicate_registration(client: TestClient):
    register_test_user(client)

    response = client.post("/auth/register", json=TEST_USER)

    assert response.status_code == 409


def test_reject_short_registration_password(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "email": "short-password@example.com",
            "password": "short",
            "display_name": "Short Password",
        },
    )

    assert response.status_code == 422


def test_login_sets_httponly_cookie(client: TestClient):
    register_test_user(client)

    response = client.post(
        "/auth/login",
        json={
            "email": TEST_USER["email"],
            "password": TEST_USER["password"],
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful."
    assert response.json()["user"]["email"] == TEST_USER["email"]

    cookie = response.cookies.get("session_token")
    assert cookie is not None

    set_cookie = response.headers.get("set-cookie", "").lower()
    assert "httponly" in set_cookie


def test_login_rejects_wrong_password(client: TestClient):
    register_test_user(client)

    response = client.post(
        "/auth/login",
        json={
            "email": TEST_USER["email"],
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401


def test_me_rejects_unauthenticated_request(client: TestClient):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_session_persists_across_requests(client: TestClient):
    register_test_user(client)

    login_response = client.post(
        "/auth/login",
        json={
            "email": TEST_USER["email"],
            "password": TEST_USER["password"],
        },
    )
    assert login_response.status_code == 200

    # TestClient retains cookies between requests, like a browser.
    response = client.get("/auth/me")

    assert response.status_code == 200
    assert response.json()["email"] == TEST_USER["email"]


def test_logout_revokes_session(client: TestClient):
    register_test_user(client)

    login_response = client.post(
        "/auth/login",
        json={
            "email": TEST_USER["email"],
            "password": TEST_USER["password"],
        },
    )
    assert login_response.status_code == 200

    me_response = client.get("/auth/me")
    assert me_response.status_code == 200

    logout_response = client.post("/auth/logout")
    assert logout_response.status_code == 200

    me_after_logout = client.get("/auth/me")
    assert me_after_logout.status_code == 401
