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
  * **Custom Swagger UI & Developer Portal** (`/docs`): Inter & JetBrains Mono typography, dark developer portal, modern HTTP method cards, and persistent Bearer token authorization.
  * **Scalar Modern API Reference** (`/scalar`): Ultra-modern interactive documentation with dark/light themes and multi-language code snippets.
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
* **Custom Swagger Developer Portal**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Scalar API Reference**: [http://127.0.0.1:8000/scalar](http://127.0.0.1:8000/scalar)
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
- Root and custom documentation endpoints (`/docs`, `/scalar`)
- Full encryption / decryption and key derivation roundtrips
- User registration, login, and encrypted Todo management
- Authenticated WebSocket communication

---

## 🚀 Live Cloud Deployment & CI/CD on Render

The repository is pre-configured to deploy automatically to **Render** via Infrastructure-as-Code ([`render.yaml`](render.yaml)) and automated GitHub Actions ([`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml)).

### 1. Initial Blueprint Setup on Render
1. Log in to [Render Dashboard](https://dashboard.render.com).
2. Click **New +** -> **Blueprint**.
3. Connect your GitHub repository (`simple_fastapi_api`).
4. Render detects [`render.yaml`](render.yaml) and provisions:
   - **`fastapi-postgres-db`**: Free Managed PostgreSQL 16 database.
   - **`fastapi-core-api`**: Production Dockerized FastAPI container.
5. Click **Apply**. Once built, your API will be live at:
   - **Live Root**: `https://<your-service-name>.onrender.com/`
   - **Live Swagger Developer Portal**: `https://<your-service-name>.onrender.com/docs`
   - **Live Scalar API Reference**: `https://<your-service-name>.onrender.com/scalar`
   - **Live Admin Dashboard**: `https://<your-service-name>.onrender.com/admin`
   - **Live WebSocket Sender Client**: `https://<your-service-name>.onrender.com/static/sender.html`
   - **Live WebSocket Receiver Client**: `https://<your-service-name>.onrender.com/static/receiver.html`

### 2. Connect Continuous Deployment (CD) Webhook
To have GitHub Actions automatically deploy whenever code is pushed:
1. In your Render Dashboard, open your web service (`fastapi-core-api`).
2. Go to **Settings** -> Scroll down to **Deploy Hook**.
3. Click **Create Deploy Hook** (or copy the existing URL):
   ```text
   https://api.render.com/deploy/srv-xxxxxxxxxxxx?key=yyyyyyyyyy
   ```
4. In your GitHub repository, navigate to:
   **Settings** ➔ **Secrets and variables** ➔ **Actions** ➔ **New repository secret**
   - **Name**: `RENDER_DEPLOY_HOOK_URL`
   - **Value**: *(Paste your copied Render Deploy Hook URL)*
5. Click **Add secret**.

### 3. How the Automated CI/CD Pipeline Works
Every time you push or merge to `main` or `master`:
1. **Stage 1 (Pytest)**: Runs tests inside GitHub Actions. If tests fail, the pipeline halts immediately.
2. **Stage 2 (Docker Build)**: Verifies that the production Docker container builds cleanly.
3. **Stage 3 (Render Deploy)**: Pings your Render Deploy Hook URL via `curl`, prompting Render to pull the verified code and perform a zero-downtime rolling update.
