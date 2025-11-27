"""
Famous Charts API Endpoints
Reference charts from notable personalities.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime

from app.core.data.famous_charts import (
    get_famous_chart,
    list_famous_charts,
    get_categories,
    search_famous_charts,
    FamousChart,
)


router = APIRouter()


class FamousChartResponse(BaseModel):
    """Famous chart response model"""
    key: str
    name: str
    birth_date: str
    birth_place: str
    latitude: float
    longitude: float
    timezone: float
    category: str
    description: str


class FamousChartListItem(BaseModel):
    """List item for famous charts"""
    key: str
    name: str
    birth_date: str
    birth_place: str
    category: str
    description: str


@router.get("/list", response_model=List[FamousChartListItem])
async def list_charts(
    category: Optional[str] = Query(None, description="Filter by category")
):
    """
    List all famous charts.
    Optionally filter by category (Politics, Science, Spiritual, Entertainment, Sports, Business).
    """
    charts = list_famous_charts(category)
    return charts


@router.get("/categories", response_model=List[str])
async def get_chart_categories():
    """Get list of available categories"""
    return get_categories()


@router.get("/search", response_model=List[FamousChartListItem])
async def search_charts(
    q: str = Query(..., description="Search query")
):
    """Search famous charts by name or description"""
    return search_famous_charts(q)


@router.get("/{chart_key}", response_model=FamousChartResponse)
async def get_chart(chart_key: str):
    """
    Get full details for a specific famous chart.
    Use the key from the list endpoint.
    """
    chart = get_famous_chart(chart_key)
    
    if not chart:
        raise HTTPException(status_code=404, detail=f"Chart '{chart_key}' not found")
    
    return FamousChartResponse(
        key=chart_key,
        name=chart.name,
        birth_date=chart.birth_date.isoformat(),
        birth_place=chart.birth_place,
        latitude=chart.latitude,
        longitude=chart.longitude,
        timezone=chart.timezone,
        category=chart.category,
        description=chart.description,
    )
