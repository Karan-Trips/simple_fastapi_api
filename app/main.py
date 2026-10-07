from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    redoc_url=None,  # ReDoc removed per design specifications
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
 
# Configure CORS for live environments (Render, Cloud, and web frontends)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Global Reset & Dark Canvas */
html, body {
    margin: 0 !important;
    padding: 0 !important;
    background-color: #0b0f19 !important;
    color: #f1f5f9 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
}

/* Hide default swagger topbar */
.swagger-ui .topbar {
    display: none !important;
}

/* Container Spacing */
.swagger-ui .wrapper {
    max-width: 1400px !important;
    padding: 0 24px !important;
    margin: 0 auto !important;
}

/* Hero / Info Card */
.swagger-ui .info {
    margin: 28px 0 24px 0 !important;
    background: linear-gradient(145deg, #111827 0%, #0f172a 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 18px !important;
    padding: 36px 40px !important;
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6) !important;
}

.swagger-ui .info .title {
    font-family: 'Inter', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2.2rem !important;
    color: #ffffff !important;
    letter-spacing: -0.03em !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
}

.swagger-ui .info .title small {
    background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
    color: #ffffff !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    padding: 3px 10px !important;
    border-radius: 9999px !important;
    vertical-align: middle !important;
    letter-spacing: normal !important;
}

.swagger-ui .info .title small.version-stamp {
    background: rgba(56, 189, 248, 0.15) !important;
    color: #38bdf8 !important;
    border: 1px solid rgba(56, 189, 248, 0.3) !important;
}

.swagger-ui .info .description {
    color: #cbd5e1 !important;
    font-size: 0.98rem !important;
    line-height: 1.65 !important;
    margin-top: 16px !important;
}

.swagger-ui .info .description h3 {
    color: #f8fafc !important;
    font-weight: 700 !important;
    font-size: 1.15rem !important;
    margin: 22px 0 10px 0 !important;
}

.swagger-ui .info .description p, 
.swagger-ui .info .description li {
    color: #94a3b8 !important;
    font-size: 0.95rem !important;
}

.swagger-ui .info .description a {
    color: #38bdf8 !important;
    font-weight: 600 !important;
    text-decoration: none !important;
    transition: color 0.15s ease !important;
}

.swagger-ui .info .description a:hover {
    color: #60a5fa !important;
    text-decoration: underline !important;
}

.swagger-ui .info .description code {
    background: #1e293b !important;
    color: #38bdf8 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 6px !important;
    padding: 2px 7px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
}

.swagger-ui .info hr {
    border: 0 !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
    margin: 20px 0 !important;
}

.swagger-ui .info .base-url {
    color: #64748b !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
}

/* Authorize Button & Toolbar */
.swagger-ui .scheme-container {
    background: transparent !important;
    box-shadow: none !important;
    padding: 16px 0 !important;
    border: none !important;
}

.swagger-ui .auth-wrapper {
    display: flex !important;
    justify-content: flex-end !important;
    gap: 12px !important;
}

.swagger-ui .btn.authorize {
    background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.45) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}

.swagger-ui .btn.authorize:hover {
    background: linear-gradient(135deg, #1d4ed8 0%, #4338ca 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.6) !important;
}

.swagger-ui .btn.authorize svg {
    fill: #ffffff !important;
    width: 16px !important;
    height: 16px !important;
}

/* Filter Input Box */
.swagger-ui .filter-container {
    padding: 10px 0 20px 0 !important;
}

.swagger-ui .filter-container .operation-filter-input {
    background: #1e293b !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    padding: 12px 18px !important;
    font-size: 0.95rem !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    width: 100% !important;
    box-sizing: border-box !important;
    transition: all 0.2s ease !important;
}

.swagger-ui .filter-container .operation-filter-input:focus {
    outline: none !important;
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25) !important;
}

/* Tag Headers (Sections) */
.swagger-ui .opblock-tag-section {
    margin-bottom: 28px !important;
}

.swagger-ui .opblock-tag {
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    padding: 16px 0 !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    margin-bottom: 14px !important;
}

.swagger-ui .opblock-tag small {
    color: #94a3b8 !important;
    font-size: 0.9rem !important;
    font-weight: 400 !important;
}

.swagger-ui .opblock-tag:hover {
    color: #38bdf8 !important;
}

/* Opblocks (API Endpoints) */
.swagger-ui .opblock {
    background: #111827 !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 12px !important;
    margin: 12px 0 !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    overflow: hidden !important;
}

.swagger-ui .opblock:hover {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35) !important;
    transform: translateY(-1px) !important;
}

.swagger-ui .opblock .opblock-summary {
    padding: 12px 18px !important;
    border: none !important;
}

.swagger-ui .opblock .opblock-summary-method {
    border-radius: 8px !important;
    font-weight: 800 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    min-width: 80px !important;
    padding: 7px 0 !important;
    text-shadow: none !important;
}

.swagger-ui .opblock .opblock-summary-path {
    color: #f8fafc !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

.swagger-ui .opblock .opblock-summary-description {
    color: #94a3b8 !important;
    font-size: 0.88rem !important;
}

/* Method Colors */
.swagger-ui .opblock.opblock-post {
    border-left: 4px solid #10b981 !important;
    background: rgba(16, 185, 129, 0.04) !important;
}
.swagger-ui .opblock.opblock-post .opblock-summary-method {
    background: #10b981 !important;
    color: #ffffff !important;
}

.swagger-ui .opblock.opblock-get {
    border-left: 4px solid #0284c7 !important;
    background: rgba(2, 132, 199, 0.04) !important;
}
.swagger-ui .opblock.opblock-get .opblock-summary-method {
    background: #0284c7 !important;
    color: #ffffff !important;
}

.swagger-ui .opblock.opblock-put {
    border-left: 4px solid #d97706 !important;
    background: rgba(217, 119, 6, 0.04) !important;
}
.swagger-ui .opblock.opblock-put .opblock-summary-method {
    background: #d97706 !important;
    color: #ffffff !important;
}

.swagger-ui .opblock.opblock-delete {
    border-left: 4px solid #dc2626 !important;
    background: rgba(220, 38, 38, 0.04) !important;
}
.swagger-ui .opblock.opblock-delete .opblock-summary-method {
    background: #dc2626 !important;
    color: #ffffff !important;
}

/* Opblock Body (Expanded View) */
.swagger-ui .opblock-body {
    background: #0f172a !important;
    padding: 24px !important;
    border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
}

.swagger-ui .opblock-section-header {
    background: #1e293b !important;
    border-radius: 8px !important;
    padding: 10px 16px !important;
    box-shadow: none !important;
}

.swagger-ui .opblock-section-header h4 {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
}

.swagger-ui .tabheader li {
    color: #94a3b8 !important;
}
.swagger-ui .tabheader li.active {
    color: #38bdf8 !important;
}

.swagger-ui table thead tr th {
    color: #94a3b8 !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.swagger-ui table tbody tr td {
    color: #cbd5e1 !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04) !important;
}

.swagger-ui .parameters-col_name {
    color: #38bdf8 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.swagger-ui .parameters-col_description p {
    color: #94a3b8 !important;
}

.swagger-ui input[type=text], 
.swagger-ui input[type=password], 
.swagger-ui textarea, 
.swagger-ui select {
    background: #1e293b !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.swagger-ui .btn.try-out__btn {
    background: #1e293b !important;
    border: 1px solid rgba(56, 189, 248, 0.4) !important;
    color: #38bdf8 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 6px 16px !important;
    transition: all 0.2s ease !important;
}

.swagger-ui .btn.try-out__btn:hover {
    background: rgba(56, 189, 248, 0.15) !important;
}

.swagger-ui .btn.execute {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35) !important;
}

.swagger-ui .btn.btn-clear {
    background: #334155 !important;
    color: #f1f5f9 !important;
    border: none !important;
    border-radius: 8px !important;
}

.swagger-ui .responses-inner {
    background: #111827 !important;
    border-radius: 12px !important;
    padding: 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
}

.swagger-ui .responses-table {
    background: transparent !important;
}

.swagger-ui .response-col_status {
    color: #10b981 !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.swagger-ui .response-col_description__inner div.markdown p {
    color: #cbd5e1 !important;
}

.swagger-ui .highlight-code {
    background: #090d16 !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 10px !important;
}

.swagger-ui .microlight {
    font-family: 'JetBrains Mono', monospace !important;
    color: #f1f5f9 !important;
    font-size: 0.9rem !important;
}

/* Models / Schemas Section */
.swagger-ui section.models {
    background: #111827 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    margin: 36px 0 !important;
}

.swagger-ui section.models h4 {
    color: #ffffff !important;
    font-weight: 700 !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
    padding: 16px 20px !important;
}

.swagger-ui .model-box {
    background: #0f172a !important;
    border-radius: 8px !important;
}

.swagger-ui .model {
    color: #cbd5e1 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.swagger-ui .model-title {
    color: #38bdf8 !important;
    font-weight: 700 !important;
}

.swagger-ui .prop-type {
    color: #34d399 !important;
}

/* Authorize Modal Popup */
.swagger-ui .dialog-ux .backdrop-ux {
    background: rgba(0, 0, 0, 0.8) !important;
    backdrop-filter: blur(8px) !important;
}

.swagger-ui .dialog-ux .modal-ux {
    background: #111827 !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 18px !important;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8) !important;
}

.swagger-ui .modal-ux-header {
    border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding: 18px 24px !important;
}

.swagger-ui .modal-ux-header h3 {
    color: #ffffff !important;
    font-weight: 800 !important;
}

.swagger-ui .modal-ux-content {
    padding: 24px !important;
}

.swagger-ui .modal-ux-content h4 {
    color: #38bdf8 !important;
    font-weight: 700 !important;
}

.swagger-ui .modal-ux-content p, 
.swagger-ui .modal-ux-content label {
    color: #94a3b8 !important;
}

.swagger-ui .modal-ux-content input {
    background: #1e293b !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    font-size: 0.95rem !important;
}

.swagger-ui .btn.modal-btn.auth {
    background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 10px 24px !important;
}

.swagger-ui .btn.modal-btn.btn-done {
    background: #334155 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
}
"""

PORTAL_HEADER_HTML = """
<div id="custom-portal-header" style="
    background: linear-gradient(90deg, #090d16 0%, #111827 50%, #0f172a 100%);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding: 14px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    position: sticky;
    top: 0;
    z-index: 9999;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
">
    <div style="display: flex; align-items: center; gap: 12px;">
        <div style="
            width: 36px; height: 36px; border-radius: 10px;
            background: linear-gradient(135deg, #38bdf8 0%, #2563eb 100%);
            display: flex; align-items: center; justify-content: center;
            font-weight: 800; color: #ffffff; font-size: 1.15rem;
            box-shadow: 0 0 16px rgba(56, 189, 248, 0.45);
        ">⚡</div>
        <div>
            <div style="font-weight: 800; font-size: 1.1rem; color: #ffffff; letter-spacing: -0.02em;">
                FastAPI Cryptographic Core
            </div>
            <div style="font-size: 0.75rem; color: #94a3b8; display: flex; gap: 8px; align-items: center; margin-top: 2px;">
                <span style="color: #38bdf8; font-weight: 700;">v2.0.0</span>
                <span>•</span>
                <span style="background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 1px 6px; border-radius: 4px; font-weight: 700; font-size: 0.7rem;">PRODUCTION</span>
                <span>•</span>
                <span>OAS 3.1</span>
            </div>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
        <a href="/scalar" target="_blank" style="
            background: rgba(255, 255, 255, 0.05); color: #e2e8f0; text-decoration: none;
            padding: 8px 16px; border-radius: 8px; font-size: 0.85rem; font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.12); display: flex; align-items: center; gap: 6px;
            transition: all 0.2s ease;
        ">
            ✨ Scalar Reference
        </a>
        <a href="/admin" target="_blank" style="
            background: rgba(255, 255, 255, 0.05); color: #e2e8f0; text-decoration: none;
            padding: 8px 16px; border-radius: 8px; font-size: 0.85rem; font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.12); display: flex; align-items: center; gap: 6px;
            transition: all 0.2s ease;
        ">
            📊 Admin Panel
        </a>
        <a href="/static/sender.html" target="_blank" style="
            background: rgba(255, 255, 255, 0.05); color: #e2e8f0; text-decoration: none;
            padding: 8px 16px; border-radius: 8px; font-size: 0.85rem; font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.12); display: flex; align-items: center; gap: 6px;
            transition: all 0.2s ease;
        ">
            💬 WebSockets
        </a>
        <a href="/health" target="_blank" style="
            background: rgba(16, 185, 129, 0.15); color: #34d399; text-decoration: none;
            padding: 8px 16px; border-radius: 8px; font-size: 0.85rem; font-weight: 700;
            border: 1px solid rgba(16, 185, 129, 0.35); display: flex; align-items: center; gap: 6px;
        ">
            💚 /health
        </a>
    </div>
</div>
"""

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    response = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{settings.PROJECT_NAME} - Developer Portal",
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
    raw_html = response.body.decode("utf-8")
    
    # Inject Google Fonts and Custom Dark Styling
    fonts_and_css = f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>{CUSTOM_SWAGGER_CSS}</style>
    """
    
    modified_html = raw_html.replace("</head>", f"{fonts_and_css}</head>")
    modified_html = modified_html.replace("<body>", f"<body>{PORTAL_HEADER_HTML}")
    return HTMLResponse(content=modified_html)


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
