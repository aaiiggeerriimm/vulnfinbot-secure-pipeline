import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "healthy"}

def test_chat_success(client):
    res = client.post("/api/chat", json={"message": "How can I manage my monthly budget?"})
    assert res.status_code == 200
    data = res.get_json()
    assert "response" in data
    assert "income" in data["response"].lower()

def test_chat_empty_message(client):
    res = client.post("/api/chat", json={"message": "   "})
    assert res.status_code == 400

def test_chat_missing_message(client):
    res = client.post("/api/chat", json={"query": "hello"})
    assert res.status_code == 400

def test_chat_invalid_json(client):
    res = client.post("/api/chat", data="not-json", content_type="application/json")
    assert res.status_code == 400

def test_chat_excessively_long_message(client):
    long_msg = "A" * 501
    res = client.post("/api/chat", json={"message": long_msg})
    assert res.status_code == 400

def test_chat_unexpected_input_type(client):
    res = client.post("/api/chat", json={"message": ["list", "instead", "of", "string"]})
    assert res.status_code == 400