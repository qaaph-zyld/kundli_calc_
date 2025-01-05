from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.kundli import (
    KundliRequest,
    KundliResponse,
    KundliPredictions,
    TransitRequest,
    TransitResponse,
    MatchingRequest,
    MatchingResponse,
)
from app.core.engine.calculator import KundliCalculator
from app.core.engine.predictor import KundliPredictor
from app.core.engine.matcher import KundliMatcher
from app.db.repositories.kundli import KundliRepository
from app.core.security import get_current_user
from app.models.user import UserInDB

router = APIRouter()
calculator = KundliCalculator()
predictor = KundliPredictor()
matcher = KundliMatcher()

@router.post("/calculate", response_model=KundliResponse)
async def calculate_kundli(
    request: KundliRequest,
    current_user: UserInDB = Depends(get_current_user),
):
    try:
        # Calculate all requested charts
        charts = calculator.calculate_all_charts(request)
        
        # Save to database
        kundli = await KundliRepository.create_kundli(
            current_user.id, request
        )
        
        return kundli
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate kundli: {str(e)}"
        )

@router.get("/{kundli_id}", response_model=KundliResponse)
async def get_kundli(
    kundli_id: str,
    current_user: UserInDB = Depends(get_current_user),
):
    kundli = await KundliRepository.get_kundli(kundli_id)
    if not kundli:
        raise HTTPException(
            status_code=404,
            detail="Kundli not found"
        )
    return kundli

@router.get("/user/list", response_model=List[KundliResponse])
async def list_user_kundlis(
    skip: int = 0,
    limit: int = 10,
    current_user: UserInDB = Depends(get_current_user),
):
    kundlis = await KundliRepository.list_user_kundlis(
        current_user.id, skip, limit
    )
    return kundlis

@router.post("/{kundli_id}/predict", response_model=KundliPredictions)
async def generate_predictions(
    kundli_id: str,
    current_user: UserInDB = Depends(get_current_user),
):
    # Check if user has premium access
    if current_user.role != "premium":
        raise HTTPException(
            status_code=403,
            detail="Premium subscription required for predictions"
        )

    kundli = await KundliRepository.get_kundli(kundli_id)
    if not kundli:
        raise HTTPException(
            status_code=404,
            detail="Kundli not found"
        )

    try:
        # Generate predictions for the main chart
        predictions = predictor.generate_predictions(kundli.charts[0])
        
        # Save predictions
        saved_predictions = await KundliRepository.save_predictions(
            kundli_id,
            KundliPredictions(
                kundli_id=kundli_id,
                predictions=predictions,
            ),
        )
        
        return saved_predictions
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate predictions: {str(e)}"
        )

@router.post("/transit", response_model=TransitResponse)
async def calculate_transit(
    request: TransitRequest,
    current_user: UserInDB = Depends(get_current_user),
):
    # Check if user has premium access
    if current_user.role != "premium":
        raise HTTPException(
            status_code=403,
            detail="Premium subscription required for transit analysis"
        )

    birth_kundli = await KundliRepository.get_kundli(request.birth_kundli_id)
    if not birth_kundli:
        raise HTTPException(
            status_code=404,
            detail="Birth kundli not found"
        )

    try:
        # Create transit kundli request
        transit_request = KundliRequest(
            date=request.transit_date,
            latitude=birth_kundli.request.latitude,
            longitude=birth_kundli.request.longitude,
            timezone=birth_kundli.request.timezone,
            chart_types=request.chart_types,
        )

        # Calculate transit charts
        transit_charts = calculator.calculate_all_charts(transit_request)

        # Generate transit predictions
        predictions = predictor.generate_predictions(transit_charts[0])

        response = TransitResponse(
            birth_kundli=birth_kundli,
            transit_charts=transit_charts,
            aspects=[],  # Calculate aspects between birth and transit planets
            predictions=predictions,
        )

        # Save transit analysis
        saved_transit = await KundliRepository.save_transit(request, response)
        return saved_transit
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate transit: {str(e)}"
        )

@router.post("/match", response_model=MatchingResponse)
async def match_kundlis(
    request: MatchingRequest,
    current_user: UserInDB = Depends(get_current_user),
):
    # Check if user has premium access
    if current_user.role != "premium":
        raise HTTPException(
            status_code=403,
            detail="Premium subscription required for matching"
        )

    # Get both kundlis
    kundli1 = await KundliRepository.get_kundli(request.kundli1_id)
    kundli2 = await KundliRepository.get_kundli(request.kundli2_id)

    if not kundli1 or not kundli2:
        raise HTTPException(
            status_code=404,
            detail="One or both kundlis not found"
        )

    try:
        # Calculate compatibility
        response = matcher.calculate_compatibility(kundli1, kundli2)

        # Save matching results
        saved_matching = await KundliRepository.save_matching(request, response)
        return saved_matching
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate compatibility: {str(e)}"
        )
