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
    charts, health, birth_charts, horoscope, dasha,
    ashtakavarga, bhava, prediction, shadbala, ayanamsa,
    kundli
)
from .api.routes import auth, kundli as kundli_routes
from .core.config import settings
from .core.errors.handlers import ErrorHandler
from .core.middleware.config import MiddlewareConfig
from .db.mongodb import MongoDB

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
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

# Configure middleware
middleware_config = MiddlewareConfig(app)
middleware_config.configure_middleware()

# Include routers
app.include_router(
    horoscope.router,
    prefix="/api",
    tags=["horoscope"]
)

app.include_router(
    charts.router,
    prefix="/api/v1/charts",
    tags=["charts"]
)

app.include_router(
    birth_charts.router,
    prefix="/api/v1/birth-charts",
    tags=["birth-charts"]
)

app.include_router(
    dasha.router,
    prefix="/api/v1/dasha",
    tags=["dasha"]
)

app.include_router(
    ashtakavarga.router,
    prefix="/api/v1/ashtakavarga",
    tags=["ashtakavarga"]
)

app.include_router(
    bhava.router,
    prefix="/api/v1/bhava",
    tags=["bhava"]
)

app.include_router(
    prediction.router,
    prefix="/api/v1/prediction",
    tags=["prediction"]
)

app.include_router(
    shadbala.router,
    prefix="/api/v1/shadbala",
    tags=["shadbala"]
)

app.include_router(
    ayanamsa.router,
    prefix="/api/v1/ayanamsa",
    tags=["ayanamsa"]
)

app.include_router(
    health.router,
    prefix="/api/v1/health",
    tags=["health"]
)

# Include new authentication and kundli routes
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["authentication"]
)

app.include_router(
    kundli_routes.router,
    prefix="/api/v1/kundli",
    tags=["kundli"]
)

@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on startup."""
    await MongoDB.connect_to_database()

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
