# 🚀 Simple FastAPI Core & Cryptographic Suite

A modern, high-performance **FastAPI** application featuring enterprise-grade **AES-256 encryption & decryption**, JWT authentication, SQLModel ORM, real-time WebSockets, and custom interactive Swagger UI & Scalar documentation.

---

## 🏗️ Architecture & Project Structure

The project follows an industry-standard **Layered Clean Architecture** separating configuration, data models, business logic, presentation routes, and utilities:

```text
simple_fastapi_api/
├── app/
│   ├── core/                  # Core foundations (Config, Database, Security & Crypto)
│   │   ├── config.py          # Pydantic Settings & environment variables (.env)
│   │   ├── database.py        # Engine, Session generator & table initialization
│   │   ├── security.py        # Password hashing, JWT token generation & OAuth2/Bearer auth
│   │   └── crypto.py          # AES-256 Fernet, AES-GCM AEAD, PBKDF2 & Hash functions
│   │
│   ├── models/                # Database entities (SQLModel / SQLAlchemy ORM)
│   │   ├── user.py            # User entity with active status and timestamps
│   │   └── todo.py            # Todo entity with encrypted secret_note support
│   │
│   ├── schemas/               # Pydantic validation models & Data Transfer Objects (DTOs)
│   │   ├── common.py          # BaseResponse generic envelope
│   │   ├── user.py            # UserCreate, UserLogin, UserRead, etc.
│   │   ├── todo.py            # TodoCreate, TodoUpdate, TodoRead
│   │   ├── crypto.py          # EncryptRequest, DecryptRequest, HashRequest
│   │   └── token.py           # Token & TokenData schemas
│   │
│   ├── services/              # Business logic & repository access layer (Service Layer)
│   │   ├── user_service.py    # User business operations & queries
│   │   ├── todo_service.py    # Task operations & encrypted note handling
│   │   └── crypto_service.py  # High-level encryption/decryption operations
│   │
│   ├── api/                   # Presentation layer (HTTP & WebSocket routes)
│   │   ├── v1/                # Versioned REST API routes
│   │   │   ├── auth.py        # /register, /login, /logout
│   │   │   ├── users.py       # /users, /users/{id}
│   │   │   ├── todos.py       # /todos, /todos/{id}
│   │   │   └── crypto.py      # /crypto/encrypt, /crypto/decrypt, /crypto/hash
│   │   └── websockets/        # Real-time WebSocket handlers
│   │       ├── manager.py     # ConnectionManager for active sessions
│   │       └── endpoint.py    # /ws endpoint
│   │
│   ├── admin/                 # SQLAdmin Control Center
│   │   └── views.py           # UserAdmin, TodoAdmin model views
│   │
│   ├── utils/                 # Utilities & helpers
│   │   └── response.py        # JSONResponse factories with jsonable_encoder
│   │
│   ├── static/                # Static assets & WebSocket test clients
│   │   ├── sender.html        # WebSocket sender client
│   │   └── receiver.html      # WebSocket receiver client
│   │
│   └── main.py                # App entrypoint, lifespan, Swagger UI & middleware
│
├── tests/                     # Automated test suites (pytest)
│   ├── test_api.py            # Full API, Crypto, Auth & WebSocket tests
│   └── test_architecture.py   # Architecture & backward-compatibility tests
│
├── requirements.txt           # Clean pinned dependencies (Python 3.9+ compatible)
├── .env.example               # Environment variables template
└── README.md                  # Project documentation
```

---

## 🌟 Highlights & Features

* 🛡️ **Military-Grade Encryption & Decryption**:
  * **AES-256 Symmetric Encryption (Fernet)**: Automatic authenticated encryption for confidential text and database fields.
  * **AES-256-GCM AEAD**: Authenticated Encryption with Associated Data (NIST-compliant).
  * **PBKDF2-HMAC-SHA256**: Human-readable passphrase-based key derivation.
  * **Cryptographic Hashes**: SHA-256, SHA-512, and HMAC-SHA256 digests.
* 📖 **Enhanced Interactive Documentation**:
  * **Custom Swagger UI** (`/docs`): Inter typography, dark topbar, modern HTTP method cards, and persistent Bearer token authorization.
  * **Scalar Modern API Reference** (`/scalar`): Ultra-modern interactive documentation with dark/light themes and multi-language code snippets.
  * **ReDoc** (`/redoc`): Clean publication-style API reference.
* 🔐 **Secure Authentication & RBAC**:
  * Bcrypt password hashing.
  * Signed JWT tokens with configurable expiration.
  * Integration with Swagger UI's **Authorize** button.
* 📝 **Task Management with Field-Level Encryption**:
  * Todo items support confidential `secret_note` fields stored as AES-256 ciphertext in the database and decrypted on retrieval.
* 📊 **SQLAdmin Dashboard** (`/admin`):
  * Web-based database management interface with search, sorting, and user/todo views.
* ⚡ **Real-Time WebSockets** (`/ws`):
  * Multi-client authenticated message broadcasting.
* ⚙️ **Resilient Configuration**:
  * Powered by `pydantic-settings` and `.env`.
  * Zero-setup SQLite default with instant switch to PostgreSQL or MySQL.

---

## 🚀 Quick Start

### 1. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables (Optional)

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

To generate a fresh 256-bit AES encryption key:
```bash
python -c "from app.core.crypto import generate_encryption_key; print(generate_encryption_key())"
```

### 3. Run Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

* **API Root**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Custom Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Scalar API Reference**: [http://127.0.0.1:8000/scalar](http://127.0.0.1:8000/scalar)
* **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
* **Admin Panel**: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
* **WebSocket Test Sender**: [http://127.0.0.1:8000/static/sender.html](http://127.0.0.1:8000/static/sender.html)
* **WebSocket Test Receiver**: [http://127.0.0.1:8000/static/receiver.html](http://127.0.0.1:8000/static/receiver.html)

---

## 🛡️ Cryptography Endpoints Guide

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/crypto/generate-key` | `GET` | Generates a fresh URL-safe 256-bit Fernet / AES key. |
| `/crypto/encrypt` | `POST` | Encrypts plaintext via server key, custom key, or user passphrase. |
| `/crypto/decrypt` | `POST` | Decrypts ciphertext back to plaintext. |
| `/crypto/aes-gcm/encrypt` | `POST` | Encrypts data using AES-256-GCM AEAD with nonce & auth tag. |
| `/crypto/aes-gcm/decrypt` | `POST` | Decrypts AES-256-GCM ciphertext and validates authentication tag. |
| `/crypto/hash` | `POST` | Computes SHA-256, SHA-512, or HMAC-SHA256 digests. |

---

## 🧪 Running Automated Tests

Run the test suite with pytest:

```bash
pytest -v tests/
```

All test suites verify:
- Clean modular architecture imports and backward compatibility adapters
- Root and custom documentation endpoints (`/docs`, `/scalar`, `/redoc`)
- Full encryption / decryption and key derivation roundtrips
- User registration, login, and encrypted Todo management
- Authenticated WebSocket communication
