"""
Kundli Calculation Service Main Application
PGF Protocol: APP_001
Gate: GATE_4
Version: 1.0.0
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import yaml
from pathlib import Path

from .api.endpoints import (
    charts, health, ayanamsa, panchang, dasha, geo, divisional
)
from .core.config import settings
from .core.errors.handlers import ErrorHandler
from .db.mongodb import MongoDB

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3100",
        "http://127.0.0.1:3100",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load custom OpenAPI schema
def custom_openapi():
    openapi_path = Path(__file__).parent / "api" / "openapi.yaml"
    if app.openapi_schema:
        return app.openapi_schema
    
    with open(openapi_path) as f:
        openapi_schema = yaml.safe_load(f)
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error handlers
app.add_exception_handler(Exception, ErrorHandler.handle_generic_exception)
app.add_exception_handler(HTTPException, ErrorHandler.handle_http_exception)

# Middleware temporarily disabled for endpoint validation

# Include routers
app.include_router(
    charts.router,
    prefix="/api/v1/charts",
    tags=["charts"]
)

app.include_router(
    ayanamsa.router,
    prefix="/api/v1/ayanamsa",
    tags=["ayanamsa"]
)

app.include_router(
    panchang.router,
    prefix="/api/v1/panchang",
    tags=["panchang"]
)

app.include_router(
    health.router,
    prefix="/api/v1/health",
    tags=["health"]
)

app.include_router(
    dasha.router,
    prefix="/api/v1",
    tags=["dasha"]
)

app.include_router(
    geo.router,
    prefix="/api/v1",
    tags=["geo"]
)

app.include_router(
    divisional.router,
    prefix="/api/v1",
    tags=["divisional"]
)

# Include new authentication and kundli routes

@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on startup."""
    try:
        await MongoDB.connect_to_database()
    except Exception:
        pass

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown."""
    await MongoDB.close_database_connection()

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to South Indian Kundli Calculator API",
        "version": "0.1.0",
        "docs": "/api/docs",
        "redoc": "/api/redoc"
    }
