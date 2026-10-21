from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_register_and_login():
    email = "pytest_user@example.com"
    password = "securepassword123"
    
    # Try registering test user
    response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "full_name": "PyTest User"}
    )
    # 201 Created or 400 Bad Request (if user already exists from prior test runs)
    assert response.status_code in [201, 400]

    # Test login to get JWT token
    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"