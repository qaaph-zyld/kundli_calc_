"""
API Router Configuration
PGF Protocol: API_001
Gate: GATE_4
Version: 1.0.0
"""

from fastapi import APIRouter
from app.api.v1.endpoints.health import router_health
from app.api.v1.endpoints.kundli import router as kundli_router
from app.api.v1.endpoints.login import login
from app.api.v1.endpoints.users import users
from app.api.v1.endpoints.birth_charts import birth_charts

api_router = APIRouter()

# Include health check router
api_router.include_router(router_health, tags=["health"])

# Include kundli router
api_router.include_router(kundli_router, prefix="/kundli", tags=["kundli"])

# Include login router
api_router.include_router(login.router, tags=["login"])

# Include users router
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Include birth charts router
api_router.include_router(birth_charts.router, prefix="/birth-charts", tags=["birth-charts"])
