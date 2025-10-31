"""
Repository Framework
PGF Protocol: STORAGE_002
Gate: GATE_4
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Type, TypeVar, Generic
from pydantic import BaseModel
from datetime import datetime
from .engine import StorageEngine, StorageQuery, QueryOperator
from .engine import kundli_storage, pattern_storage

T = TypeVar("T", bound=BaseModel)

class Repository(Generic[T]):
    """Generic repository for data access"""
    
    def __init__(self, storage: StorageEngine, model: Type[T]):
        self.storage = storage
        self.model = model
    
    async def create(self, data: T) -> str:
        """Create new entity"""
        document = data.dict()
        document["created_at"] = datetime.utcnow()
        document["updated_at"] = document["created_at"]
        
        return await self.storage.insert_one(document)
    
    async def create_many(self, items: List[T]) -> List[str]:
        """Create multiple entities"""
        documents = []
        now = datetime.utcnow()
        
        for item in items:
            document = item.dict()
            document["created_at"] = now
            document["updated_at"] = now
            documents.append(document)
        
        return await self.storage.insert_many(documents)
    
    async def find_by_id(self, id: str) -> Optional[T]:
        """Find entity by ID"""
        query = StorageQuery(
            filters={"_id": {QueryOperator.EQ: id}}
        )
        
        return await self.storage.find_one(query, self.model)
    
    async def find_one(
        self,
        filters: Dict[str, Dict[str, Any]],
        projection: Optional[List[str]] = None
    ) -> Optional[T]:
        """Find single entity by filters"""
        query = StorageQuery(
            filters=filters,
            projection=projection
        )
        
        return await self.storage.find_one(query, self.model)
    
    async def find_many(
        self,
        filters: Optional[Dict[str, Dict[str, Any]]] = None,
        sort: Optional[Dict[str, int]] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        projection: Optional[List[str]] = None
    ) -> List[T]:
        """Find multiple entities by filters"""
        query = StorageQuery(
            filters=filters or {},
            sort=sort,
            skip=skip,
            limit=limit,
            projection=projection
        )
        
        return await self.storage.find_many(query, self.model)
    
    async def update(self, id: str, data: Dict[str, Any]) -> bool:
        """Update entity by ID"""
        query = StorageQuery(
            filters={"_id": {QueryOperator.EQ: id}}
        )
        
        update_data = {
            **data,
            "updated_at": datetime.utcnow()
        }
        
        return await self.storage.update_one(query, update_data)
    
    async def update_many(
        self,
        filters: Dict[str, Dict[str, Any]],
        data: Dict[str, Any]
    ) -> int:
        """Update multiple entities by filters"""
        query = StorageQuery(filters=filters)
        
        update_data = {
            **data,
            "updated_at": datetime.utcnow()
        }
        
        return await self.storage.update_many(query, update_data)
    
    async def delete(self, id: str) -> bool:
        """Delete entity by ID"""
        query = StorageQuery(
            filters={"_id": {QueryOperator.EQ: id}}
        )
        
        return await self.storage.delete_one(query)
    
    async def delete_many(self, filters: Dict[str, Dict[str, Any]]) -> int:
        """Delete multiple entities by filters"""
        query = StorageQuery(filters=filters)
        
        return await self.storage.delete_many(query)
    
    async def count(self, filters: Optional[Dict[str, Dict[str, Any]]] = None) -> int:
        """Count entities by filters"""
        query = StorageQuery(filters=filters or {})
        documents = await self.storage.find_many(query)
        return len(documents)

class KundliData(BaseModel):
    """Kundli data model"""
    
    id: Optional[str] = None
    date: str
    time: str
    latitude: float
    longitude: float
    timezone: str
    planets: Dict[str, Any]
    houses: Dict[str, Any]
    aspects: List[Dict[str, Any]]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PatternData(BaseModel):
    """Pattern data model"""
    
    id: Optional[str] = None
    kundli_id: str
    yogas: List[Dict[str, Any]]
    raja_yogas: List[Dict[str, Any]]
    dhana_yogas: List[Dict[str, Any]]
    malefic_patterns: List[Dict[str, Any]]
    benefic_patterns: List[Dict[str, Any]]
    analysis: Dict[str, Any]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Global repository instances
kundli_repository = Repository[KundliData](
    storage=kundli_storage,
    model=KundliData
)

pattern_repository = Repository[PatternData](
    storage=pattern_storage,
    model=PatternData
)
