import pytest
import httpx

BASE_URL = "http://localhost:8000"  # 替换为你的实际服务地址

@pytest.fixture
def client():
    return httpx.Client(base_url=BASE_URL)

# 测试获取 OpenAPI 文档
def test_get_openapi_json(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json()  # 确保返回的是有效的 JSON

# 测试 Swagger UI
def test_get_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200

# 测试用户创建
def test_create_user(client):
    user_data = {
        "user": {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        }
    }
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 200
    json_response = response.json()
    assert "user" in json_response
    assert json_response["user"]["username"] == "testuser"

# 测试用户登录
def test_user_login(client):
    login_data = {
        "user": {
            "email": "testuser@example.com",
            "password": "testpassword"
        }
    }
    response = client.post("/api/users/login", json=login_data)
    assert response.status_code == 200
    json_response = response.json()
    assert "user" in json_response
    assert "token" in json_response["user"]

# 测试获取用户信息 (需要认证)
def test_get_user(client):
    # 假设你已经有一个有效的用户 token
    token = "your_token_here"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get("/api/user", headers=headers)
    assert response.status_code == 200
    json_response = response.json()
    assert "user" in json_response
