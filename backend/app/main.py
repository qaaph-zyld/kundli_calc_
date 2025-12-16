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
    charts, health, ayanamsa, panchang, dasha, geo, divisional, debug, location, famous_charts,
    lal_kitab, varshphal, yogas, transits, kp_system, shadbala, ashtakavarga, bhava, prediction,
    additional_dashas, horoscope, compatibility
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
    allow_origins=["*"],
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

app.include_router(
    debug.router,
    prefix="/api/v1/debug",
    tags=["debug"]
)

app.include_router(
    location.router,
    prefix="/api/v1/location",
    tags=["location"]
)

app.include_router(
    famous_charts.router,
    prefix="/api/v1/famous-charts",
    tags=["famous-charts"]
)

app.include_router(
    lal_kitab.router,
    prefix="/api/v1",
    tags=["lal-kitab"]
)

app.include_router(
    varshphal.router,
    prefix="/api/v1",
    tags=["varshphal"]
)

app.include_router(
    yogas.router,
    prefix="/api/v1/yogas",
    tags=["yogas"]
)

app.include_router(
    transits.router,
    prefix="/api/v1/transits",
    tags=["transits"]
)

app.include_router(
    kp_system.router,
    prefix="/api/v1/kp",
    tags=["kp-system"]
)

app.include_router(
    shadbala.router,
    prefix="/api/v1/shadbala",
    tags=["shadbala"]
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
    additional_dashas.router,
    prefix="/api/v1/dashas",
    tags=["additional-dashas"]
)

app.include_router(
    horoscope.router,
    prefix="/api/v1/horoscope",
    tags=["horoscope"]
)

app.include_router(
    compatibility.router,
    prefix="/api/v1",
    tags=["compatibility"]
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
