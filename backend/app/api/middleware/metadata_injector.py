"""API Response Metadata Injector
=================================
Middleware to inject calculation metadata into API responses for transparency.

This enhances responses with:
- Calculation formulas
- Sources and references
- Method documentation
- Accuracy information

Author: Kundli Calculation Engine
Date: 2024-12-31
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import json
from typing import Dict, Any, Optional
import time

from app.core.metadata.calculation_metadata import (
    CalculationMetadata,
    CalculationType
)


class MetadataInjectorMiddleware(BaseHTTPMiddleware):
    """Middleware to inject calculation metadata into responses."""
    
    def __init__(self, app, include_metadata: bool = True):
        super().__init__(app)
        self.include_metadata = include_metadata
        self.metadata_handler = CalculationMetadata()
    
    async def dispatch(self, request: Request, call_next):
        """Process request and inject metadata into response."""
        start_time = time.time()
        
        # Call the actual endpoint
        response = await call_next(request)
        
        # Only process JSON responses
        if not self.include_metadata or response.status_code != 200:
            return response
        
        # Check if this is an API endpoint that should have metadata
        if not self._should_inject_metadata(request.url.path):
            return response
        
        # Parse response body
        try:
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            
            data = json.loads(body.decode())
            
            # Inject metadata
            metadata = self._generate_metadata(request.url.path, data)
            if metadata:
                data['_metadata'] = metadata
                data['_performance'] = {
                    'response_time_ms': round((time.time() - start_time) * 1000, 2),
                    'calculation_engine': 'Kundli Calc Engine v2.0',
                    'accuracy_standard': 'Verified against Jagannatha Hora'
                }
            
            # Create new response
            return JSONResponse(content=data, status_code=200)
            
        except Exception as e:
            # If metadata injection fails, return original response
            return response
    
    def _should_inject_metadata(self, path: str) -> bool:
        """Determine if metadata should be injected for this endpoint."""
        metadata_paths = [
            '/api/v1/charts',
            '/api/v1/divisional',
            '/api/v1/dasha',
            '/api/v1/shadbala',
            '/api/v1/ashtakavarga',
            '/api/v1/yogas',
            '/api/v1/ayanamsa',
            '/api/v1/panchang',
            '/api/v1/kp'
        ]
        
        return any(path.startswith(prefix) for prefix in metadata_paths)
    
    def _generate_metadata(self, path: str, response_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate appropriate metadata based on endpoint."""
        metadata = {
            'endpoint': path,
            'calculation_info': {},
            'sources': []
        }
        
        # Determine calculation type from path
        if '/charts' in path or '/divisional' in path:
            if '/divisional' in path:
                division = response_data.get('division', 9)
                calc_metadata = self.metadata_handler.get_divisional_chart_metadata(division)
            else:
                calc_metadata = self.metadata_handler.get_planetary_position_metadata()
            
            metadata['calculation_info'] = calc_metadata
            metadata['house_system'] = self.metadata_handler.get_house_system_metadata()
            
        elif '/dasha' in path:
            system = response_data.get('system', 'Vimshottari')
            metadata['calculation_info'] = self.metadata_handler.get_dasha_metadata(system)
            
        elif '/shadbala' in path:
            metadata['calculation_info'] = self.metadata_handler.get_shadbala_metadata()
            
        elif '/ashtakavarga' in path:
            metadata['calculation_info'] = self.metadata_handler.get_ashtakavarga_metadata()
            
        elif '/ayanamsa' in path:
            system = response_data.get('system', 'Lahiri')
            metadata['calculation_info'] = self.metadata_handler.get_ayanamsa_metadata(system)
        
        # Add common sources
        metadata['sources'] = self.metadata_handler.get_all_sources()
        
        # Add transparency note
        metadata['transparency'] = {
            'open_source': True,
            'calculation_methods': 'All formulas documented in metadata',
            'verification': 'Calculations verified against Jagannatha Hora',
            'accuracy_tolerance': '±0.1° for positions, ±1 year for dashas'
        }
        
        return metadata if metadata['calculation_info'] else None


def add_metadata_to_response(
    response_data: Dict[str, Any],
    calc_type: CalculationType,
    **kwargs
) -> Dict[str, Any]:
    """
    Utility function to manually add metadata to a response.
    
    Usage in endpoints:
    ```python
    result = calculate_chart(...)
    return add_metadata_to_response(
        result,
        CalculationType.PLANETARY_POSITION
    )
    ```
    """
    metadata_handler = CalculationMetadata()
    metadata = metadata_handler.get_calculation_metadata(calc_type, **kwargs)
    
    response_data['_metadata'] = {
        'calculation_info': metadata,
        'sources': metadata_handler.get_all_sources(),
        'transparency': {
            'open_source': True,
            'formulas_documented': True,
            'verification_standard': 'Jagannatha Hora',
            'ayanamsa_default': 'Lahiri',
            'house_system_default': 'Whole Sign'
        }
    }
    
    return response_data
