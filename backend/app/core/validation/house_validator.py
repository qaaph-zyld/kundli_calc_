"""
House System Validation
PGF Protocol: HOUSE_VAL_001
Gate: GATE_4
Version: 1.0.0
"""

class HouseValidationError(Exception):
    """Exception raised for house calculation validation errors"""
    pass

class HouseValidator:
    """Validator for house calculations"""
    
    def __init__(self):
        """Initialize validator"""
        # Define valid house systems
        self.valid_house_systems = {
            'PLACIDUS',
            'KOCH',
            'EQUAL',
            'WHOLE_SIGN',
            'REGIOMONTANUS',
            'CAMPANUS'
        }
    
    def validate_coordinates(
        self,
        latitude: float,
        longitude: float
    ) -> bool:
        """Validate geographical coordinates
        
        Args:
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            
        Returns:
            True if coordinates are valid
        """
        # Check latitude range (-90 to +90)
        if not -90 <= latitude <= 90:
            return False
        
        # Check longitude range (-180 to +180)
        if not -180 <= longitude <= 180:
            return False
        
        return True
    
    def validate_house_system(
        self,
        house_system: str
    ) -> bool:
        """Validate house system name
        
        Args:
            house_system: House system name
            
        Returns:
            True if house system is valid
        """
        return house_system.upper() in self.valid_house_systems
