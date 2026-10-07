from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import engine, init_db
from app.api.v1 import api_v1_router
from app.api.websockets import ws_router
from app.admin import setup_admin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# Application Lifespan
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database schema safely on startup
    logger.info("Initializing database schema...")
    init_db()
    logger.info("Application startup complete.")
    yield
    logger.info("Application shutdown initiated.")


# ============================================================================
# FastAPI Application Instance
# ============================================================================

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    lifespan=lifespan,
    docs_url=None,  # Custom enhanced Swagger UI route below
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Authentication & Users",
            "description": "🔐 User registration, JWT login/logout, and account management."
        },
        {
            "name": "Cryptography & Security",
            "description": "🛡️ Military-grade AES-256 (Fernet) encryption, AES-GCM AEAD, PBKDF2 key derivation, and hashing."
        },
        {
            "name": "Todo & Task Management",
            "description": "📝 Task creation, updates, and deletion with optional AES-256 encrypted confidential notes."
        },
        {
            "name": "Real-time WebSocket",
            "description": "⚡ Authenticated real-time message broadcasting."
        },
        {
            "name": "System & Health",
            "description": "⚙️ Health checks, API discovery, and diagnostics."
        },
    ],
)

# Include Core Routers
app.include_router(api_v1_router)
app.include_router(ws_router)

# Mount Static Assets (HTML clients for WebSocket testing)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Mount SQLAdmin Control Panel
admin = setup_admin(app, engine)


# ============================================================================
# Enhanced Swagger UI Custom Route
# ============================================================================

CUSTOM_SWAGGER_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    background: #f8fafc !important;
    color: #0f172a !important;
}

.swagger-ui .topbar {
    background: linear-gradient(135deg, #090d16 0%, #111827 50%, #1e3a8a 100%) !important;
    padding: 16px 24px !important;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.35) !important;
    border-bottom: 2px solid rgba(59, 130, 246, 0.4) !important;
}

.swagger-ui .topbar .download-url-wrapper {
    display: none !important;
}

.swagger-ui .topbar-wrapper a span {
    font-weight: 700 !important;
    font-size: 1.25rem !important;
    color: #60a5fa !important;
    letter-spacing: -0.02em !important;
}

.swagger-ui .info {
    margin: 32px 0 !important;
    background: #ffffff !important;
    padding: 28px !important;
    border-radius: 14px !important;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.03) !important;
    border-left: 6px solid #3b82f6 !important;
}

.swagger-ui .info .title {
    font-family: 'Inter', sans-serif !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    letter-spacing: -0.03em !important;
}

.swagger-ui .opblock {
    border-radius: 12px !important;
    box-shadow: 0 2px 8px -1px rgba(0, 0, 0, 0.04) !important;
    margin: 14px 0 !important;
    border: 1px solid rgba(0, 0, 0, 0.06) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    overflow: hidden !important;
}

.swagger-ui .opblock:hover {
    box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.08) !important;
}

.swagger-ui .btn.authorize {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.35) !important;
    transition: all 0.2s ease !important;
}

.swagger-ui .btn.authorize:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
    transform: translateY(-1px) !important;
}

.swagger-ui .btn.authorize svg {
    fill: #ffffff !important;
}

.swagger-ui .opblock.opblock-post {
    background: rgba(16, 185, 129, 0.04) !important;
    border-color: rgba(16, 185, 129, 0.25) !important;
}
.swagger-ui .opblock.opblock-post .opblock-summary-method {
    background: #10b981 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}

.swagger-ui .opblock.opblock-get {
    background: rgba(59, 130, 246, 0.04) !important;
    border-color: rgba(59, 130, 246, 0.25) !important;
}
.swagger-ui .opblock.opblock-get .opblock-summary-method {
    background: #3b82f6 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}

.swagger-ui .opblock.opblock-put {
    background: rgba(245, 158, 11, 0.04) !important;
    border-color: rgba(245, 158, 11, 0.25) !important;
}
.swagger-ui .opblock.opblock-put .opblock-summary-method {
    background: #f59e0b !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}

.swagger-ui .opblock.opblock-delete {
    background: rgba(239, 68, 68, 0.04) !important;
    border-color: rgba(239, 68, 68, 0.25) !important;
}
.swagger-ui .opblock.opblock-delete .opblock-summary-method {
    background: #ef4444 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}
"""

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    response = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{settings.PROJECT_NAME} - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": 1,
            "docExpansion": "list",
            "filter": True,
            "syntaxHighlight.theme": "monokai",
            "persistAuthorization": True,
            "tryItOutEnabled": True,
            "displayRequestDuration": True,
        },
    )
    html_content = response.body.decode("utf-8").replace(
        "</head>", f"<style>{CUSTOM_SWAGGER_CSS}</style></head>"
    )
    return HTMLResponse(content=html_content)


# ============================================================================
# Modern Scalar API Reference Route
# ============================================================================

@app.get("/scalar", include_in_schema=False, response_class=HTMLResponse)
async def scalar_docs():
    """Serves the Scalar interactive API reference (modern dark/light mode alternative)."""
    return f"""
    <!doctype html>
    <html>
      <head>
        <title>{settings.PROJECT_NAME} - Scalar Reference</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" type="image/svg+xml" href="https://fastapi.tiangolo.com/img/favicon.png" />
      </head>
      <body>
        <script id="api-reference" data-url="{app.openapi_url}"></script>
        <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
      </body>
    </html>
    """


# ============================================================================
# Root & Health Endpoints
# ============================================================================

@app.get("/", tags=["System & Health"], summary="API Root & Navigation")
async def root():
    return {
        "status": "online",
        "name": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT,
        "documentation": {
            "swagger_ui": "/docs",
            "scalar_ui": "/scalar",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json"
        },
        "admin_panel": "/admin",
        "static_clients": {
            "websocket_sender": "/static/sender.html",
            "websocket_receiver": "/static/receiver.html"
        },
        "features": [
            "AES-256 Symmetric Encryption & Decryption (/crypto/encrypt, /crypto/decrypt)",
            "AES-256-GCM AEAD Mode (/crypto/aes-gcm/encrypt, /crypto/aes-gcm/decrypt)",
            "PBKDF2-HMAC-SHA256 Passphrase Key Derivation",
            "JWT Bearer Authentication & User Management (/register, /login, /users)",
            "Encrypted Task Management (/todos)",
            "Real-time WebSockets (/ws)"
        ]
    }


@app.get("/health", tags=["System & Health"], summary="Health Check")
async def health_check():
    return {
        "status": "healthy",
        "database": str(engine.url.database or engine.url),
        "encryption_enabled": True
    }
