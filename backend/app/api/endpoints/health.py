"""
Health Check Endpoint
PGF Protocol: API_001
Gate: GATE_4
Version: 1.0.0
"""

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@router.get("/simulate-error")
async def simulate_error():
    """Endpoint to simulate a 500 error for testing"""
    raise HTTPException(status_code=500, detail="Simulated server error")
