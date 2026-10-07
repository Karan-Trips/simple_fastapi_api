from __future__ import annotations

import uuid
import pytest
from fastapi.testclient import TestClient

from app import database, models
from app.auth import create_access_token
from app.main import app

client = TestClient(app)


def setup_module():
    """Ensure database schema is created before tests."""
    database.init_db()


def test_root_and_docs():
    """Verify root navigation and documentation endpoints."""
    # Root
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert "/docs" in data["documentation"]["swagger_ui"]
    assert "/scalar" in data["documentation"]["scalar_ui"]
    assert "redoc" not in data["documentation"]

    # Verify ReDoc is disabled (returns 404)
    assert client.get("/redoc").status_code == 404

    # Health check
    health_res = client.get("/health")
    assert health_res.status_code == 200
    assert health_res.json()["status"] == "healthy"

    # Swagger UI HTML with custom styling and developer portal
    docs_res = client.get("/docs")
    assert docs_res.status_code == 200
    assert "Developer Portal" in docs_res.text
    assert "Inter" in docs_res.text  # Custom modern styling injected
    assert "custom-portal-header" in docs_res.text

    # Scalar HTML
    scalar_res = client.get("/scalar")
    assert scalar_res.status_code == 200
    assert "Scalar Reference" in scalar_res.text


def test_crypto_endpoints():
    """Verify all encryption, decryption, key generation, and hashing endpoints."""
    # 1. Generate Key
    key_res = client.get("/crypto/generate-key")
    assert key_res.status_code == 200
    gen_key = key_res.json()["data"]["key"]
    assert len(gen_key) > 30

    # 2. Server Key Encryption & Decryption
    secret_text = "TopSecretAPIKey_12345"
    enc_res = client.post("/crypto/encrypt", json={"text": secret_text})
    assert enc_res.status_code == 200
    ciphertext = enc_res.json()["data"]["ciphertext"]
    assert ciphertext != secret_text

    dec_res = client.post("/crypto/decrypt", json={"ciphertext": ciphertext})
    assert dec_res.status_code == 200
    assert dec_res.json()["data"]["plaintext"] == secret_text

    # 3. Custom Key Encryption & Decryption
    enc_custom = client.post("/crypto/encrypt", json={"text": secret_text, "key": gen_key})
    assert enc_custom.status_code == 200
    ct_custom = enc_custom.json()["data"]["ciphertext"]

    dec_custom = client.post("/crypto/decrypt", json={"ciphertext": ct_custom, "key": gen_key})
    assert dec_custom.status_code == 200
    assert dec_custom.json()["data"]["plaintext"] == secret_text

    # 4. Passphrase Encryption & Decryption
    passphrase = "SuperStrongPassword@999"
    enc_pass = client.post("/crypto/encrypt", json={"text": secret_text, "passphrase": passphrase})
    assert enc_pass.status_code == 200
    ct_pass = enc_pass.json()["data"]["ciphertext"]

    dec_pass = client.post("/crypto/decrypt", json={"ciphertext": ct_pass, "passphrase": passphrase})
    assert dec_pass.status_code == 200
    assert dec_pass.json()["data"]["plaintext"] == secret_text

    # Wrong passphrase should fail gracefully
    dec_fail = client.post("/crypto/decrypt", json={"ciphertext": ct_pass, "passphrase": "WrongPassword"})
    assert dec_fail.status_code == 400

    # 5. AES-256-GCM AEAD
    gcm_enc = client.post("/crypto/aes-gcm/encrypt", json={"text": secret_text, "associated_data": "header-123"})
    assert gcm_enc.status_code == 200
    gcm_data = gcm_enc.json()["data"]

    gcm_dec = client.post(
        "/crypto/aes-gcm/decrypt",
        json={
            "nonce": gcm_data["nonce"],
            "ciphertext": gcm_data["ciphertext"],
            "associated_data": "header-123"
        }
    )
    assert gcm_dec.status_code == 200
    assert gcm_dec.json()["data"]["plaintext"] == secret_text

    # 6. Hashing
    hash_sha256 = client.post("/crypto/hash", json={"text": "hello world", "algorithm": "sha256"})
    assert hash_sha256.status_code == 200
    assert len(hash_sha256.json()["data"]["digest"]) == 64

    hash_sha512 = client.post("/crypto/hash", json={"text": "hello world", "algorithm": "sha512"})
    assert hash_sha512.status_code == 200
    assert len(hash_sha512.json()["data"]["digest"]) == 128

    hash_hmac = client.post(
        "/crypto/hash", 
        json={"text": "hello world", "algorithm": "hmac_sha256", "secret": "my-secret"}
    )
    assert hash_hmac.status_code == 200


def test_auth_and_user_flow():
    """Verify registration, login, profile retrieval, and todos with encryption."""
    suffix = uuid.uuid4().hex[:6]
    username = f"user_{suffix}"
    email = f"user_{suffix}@example.com"
    password = "DevPassword123!"

    # 1. Register
    reg_res = client.post("/register", data={"name": username, "email": email, "password": password})
    assert reg_res.status_code in [200, 201]

    # Duplicate registration should return 400
    dup_res = client.post("/register", data={"name": username, "email": email, "password": password})
    assert dup_res.status_code == 400

    # 2. Login
    login_res = client.post("/login", data={"username": username, "password": password})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    assert token

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Get Users via RESTful and Legacy routes
    users_res = client.get("/users")
    assert users_res.status_code == 200
    users = users_res.json()["data"]["users"]
    user_item = next((u for u in users if u["name"] == username), None)
    assert user_item is not None
    user_id = user_item["id"]

    legacy_fetch = client.get("/fetch")
    assert legacy_fetch.status_code == 200

    # 4. Fetch User by ID (REST and Legacy)
    user_by_id = client.get(f"/users/{user_id}", headers=headers)
    assert user_by_id.status_code == 200
    assert user_by_id.json()["data"]["email"] == email

    legacy_by_id = client.post("/userId", data={"id": user_id}, headers=headers)
    assert legacy_by_id.status_code == 200

    # 5. Create Todo with encrypted note
    todo_res = client.post(
        "/todos",
        json={
            "task": "Review cryptography deployment",
            "status": False,
            "secret_note": "Confidential production key: PROD-9988-X",
            "encrypt_note": True
        },
        headers=headers
    )
    assert todo_res.status_code in [200, 201]
    todo_data = todo_res.json()["data"]
    todo_id = todo_data["id"]
    assert todo_data["is_encrypted"] is True
    # The stored secret_note in the database should be ciphertext, not plaintext!
    assert todo_data["secret_note"] != "Confidential production key: PROD-9988-X"

    # 6. Fetch Todos with auto-decryption
    fetch_todos = client.get("/todos?decrypt_notes=true", headers=headers)
    assert fetch_todos.status_code == 200
    todo_list = fetch_todos.json()["data"]["todos"]
    matching = next((t for t in todo_list if t["id"] == todo_id), None)
    assert matching is not None
    assert matching["secret_note_decrypted"] == "Confidential production key: PROD-9988-X"

    # 7. Update Todo
    update_res = client.put(
        f"/todos/{todo_id}",
        json={"task": "Review cryptography deployment (Completed)", "status": True},
        headers=headers
    )
    assert update_res.status_code == 200
    assert update_res.json()["data"]["status"] is True

    # 8. Delete Todo
    del_todo = client.delete(f"/todos/{todo_id}", headers=headers)
    assert del_todo.status_code == 200

    # 9. Logout
    logout_res = client.post("/logout", headers=headers)
    assert logout_res.status_code == 200


def test_websocket_chat():
    """Verify WebSocket endpoint with token authentication."""
    # 1. Reject without token
    with pytest.raises(Exception):
        with client.websocket_connect("/ws") as ws:
            pass

    # 2. Connect with valid token
    token = create_access_token(data={"sub": "999", "username": "alice_ws"})
    with client.websocket_connect(f"/ws?token={token}") as websocket:
        websocket.send_text("Hello from websocket test")
        data = websocket.receive_text()
        assert "alice_ws: Hello from websocket test" in data
