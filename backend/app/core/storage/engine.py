"""
Data Storage Engine
PGF Protocol: STORAGE_001
Gate: GATE_4
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Type, Union
from pydantic import BaseModel, Field
from datetime import datetime
import asyncio
from enum import Enum
import motor.motor_asyncio
from bson import ObjectId
import json
from pathlib import Path

class StorageType(str, Enum):
    """Storage types"""
    MONGODB = "mongodb"
    POSTGRESQL = "postgresql"
    REDIS = "redis"
    FILE = "file"

class StorageConfig(BaseModel):
    """Storage configuration"""
    
    type: StorageType
    connection_string: str
    database_name: str
    collection_name: Optional[str] = None
    table_name: Optional[str] = None
    options: Dict[str, Any] = Field(default_factory=dict)

class QueryOperator(str, Enum):
    """Query operators"""
    EQ = "eq"          # Equal
    NE = "ne"          # Not Equal
    GT = "gt"          # Greater Than
    GTE = "gte"        # Greater Than or Equal
    LT = "lt"          # Less Than
    LTE = "lte"        # Less Than or Equal
    IN = "in"          # In Array
    NIN = "nin"        # Not In Array
    EXISTS = "exists"  # Field Exists
    TYPE = "type"      # Field Type

class StorageQuery(BaseModel):
    """Storage query definition"""
    
    filters: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    sort: Optional[Dict[str, int]] = None
    skip: Optional[int] = None
    limit: Optional[int] = None
    projection: Optional[List[str]] = None

class StorageEngine:
    """Data storage engine"""
    
    def __init__(self, config: StorageConfig):
        self.config = config
        self._client = None
        self._db = None
        self._collection = None
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize storage engine"""
        if self._initialized:
            return
            
        if self.config.type == StorageType.MONGODB:
            await self._initialize_mongodb()
        elif self.config.type == StorageType.POSTGRESQL:
            await self._initialize_postgresql()
        elif self.config.type == StorageType.REDIS:
            await self._initialize_redis()
        elif self.config.type == StorageType.FILE:
            await self._initialize_file_storage()
            
        self._initialized = True
    
    async def _initialize_mongodb(self) -> None:
        """Initialize MongoDB connection"""
        self._client = motor.motor_asyncio.AsyncIOMotorClient(
            self.config.connection_string,
            **self.config.options
        )
        self._db = self._client[self.config.database_name]
        if self.config.collection_name:
            self._collection = self._db[self.config.collection_name]
    
    async def _initialize_postgresql(self) -> None:
        """Initialize PostgreSQL connection"""
        # Implement PostgreSQL initialization
        pass
    
    async def _initialize_redis(self) -> None:
        """Initialize Redis connection"""
        # Implement Redis initialization
        pass
    
    async def _initialize_file_storage(self) -> None:
        """Initialize file storage"""
        storage_path = Path(self.config.connection_string)
        storage_path.mkdir(parents=True, exist_ok=True)
    
    async def close(self) -> None:
        """Close storage engine connections"""
        if self.config.type == StorageType.MONGODB and self._client:
            self._client.close()
    
    async def insert_one(self, document: Dict[str, Any]) -> str:
        """Insert single document"""
        if not self._initialized:
            await self.initialize()
            
        if self.config.type == StorageType.MONGODB:
            result = await self._collection.insert_one(document)
            return str(result.inserted_id)
            
        elif self.config.type == StorageType.FILE:
            doc_id = str(ObjectId())
            file_path = Path(self.config.connection_string) / f"{doc_id}.json"
            with open(file_path, "w") as f:
                json.dump({**document, "_id": doc_id}, f)
            return doc_id
    
    async def insert_many(self, documents: List[Dict[str, Any]]) -> List[str]:
        """Insert multiple documents"""
        if not self._initialized:
            await self.initialize()
            
        if self.config.type == StorageType.MONGODB:
            result = await self._collection.insert_many(documents)
            return [str(id) for id in result.inserted_ids]
            
        elif self.config.type == StorageType.FILE:
            doc_ids = []
            for doc in documents:
                doc_id = await self.insert_one(doc)
                doc_ids.append(doc_id)
            return doc_ids
    
    async def find_one(
        self,
        query: StorageQuery,
        model: Optional[Type[BaseModel]] = None
    ) -> Optional[Union[Dict[str, Any], BaseModel]]:
        """Find single document"""
        if not self._initialized:
            await self.initialize()
            
        if self.config.type == StorageType.MONGODB:
            mongo_query = self._build_mongo_query(query)
            document = await self._collection.find_one(
                mongo_query,
                projection=dict.fromkeys(query.projection, 1) if query.projection else None
            )
            
            if document:
                document["_id"] = str(document["_id"])
                return model(**document) if model else document
            return None
            
        elif self.config.type == StorageType.FILE:
            # Implement file-based query
            pass
    
    async def find_many(
        self,
        query: StorageQuery,
        model: Optional[Type[BaseModel]] = None
    ) -> List[Union[Dict[str, Any], BaseModel]]:
        """Find multiple documents"""
        if not self._initialized:
            await self.initialize()
            
        if self.config.type == StorageType.MONGODB:
            mongo_query = self._build_mongo_query(query)
            cursor = self._collection.find(
                mongo_query,
                projection=dict.fromkeys(query.projection, 1) if query.projection else None
            )
            
            if query.sort:
                cursor = cursor.sort([(k, v) for k, v in query.sort.items()])
            
            if query.skip:
                cursor = cursor.skip(query.skip)
            
            if query.limit:
                cursor = cursor.limit(query.limit)
            
            documents = []
            async for document in cursor:
                document["_id"] = str(document["_id"])
                documents.append(model(**document) if model else document)
            
            return documents
            
        elif self.config.type == StorageType.FILE:
            # Implement file-based query
            pass
    
    async def update_one(
        self,
        query: StorageQuery,
        update: Dict[str, Any]
    ) -> bool:
        """Update single document"""
        if not self._initialized:
            await self.initialize()
            
        if self.config.type == StorageType.MONGODB:
            mongo_query = self._build_mongo_query(query)
            result = await self._collection.update_one(mongo_query, {"$set": update})
            return result.modified_count > 0
            
        elif self.config.type == StorageType.FILE:
            # Implement file-based update
            pass
    
    async def update_many(
        self,
        query: StorageQuery,
        update: Dict[str, Any]
    ) -> int:
        """Update multiple documents"""
        if not self._initialized:
            await self.initialize()
            
        if self.config.type == StorageType.MONGODB:
            mongo_query = self._build_mongo_query(query)
            result = await self._collection.update_many(mongo_query, {"$set": update})
            return result.modified_count
            
        elif self.config.type == StorageType.FILE:
            # Implement file-based update
            pass
    
    async def delete_one(self, query: StorageQuery) -> bool:
        """Delete single document"""
        if not self._initialized:
            await self.initialize()
            
        if self.config.type == StorageType.MONGODB:
            mongo_query = self._build_mongo_query(query)
            result = await self._collection.delete_one(mongo_query)
            return result.deleted_count > 0
            
        elif self.config.type == StorageType.FILE:
            # Implement file-based delete
            pass
    
    async def delete_many(self, query: StorageQuery) -> int:
        """Delete multiple documents"""
        if not self._initialized:
            await self.initialize()
            
        if self.config.type == StorageType.MONGODB:
            mongo_query = self._build_mongo_query(query)
            result = await self._collection.delete_many(mongo_query)
            return result.deleted_count
            
        elif self.config.type == StorageType.FILE:
            # Implement file-based delete
            pass
    
    def _build_mongo_query(self, query: StorageQuery) -> Dict[str, Any]:
        """Build MongoDB query from StorageQuery"""
        mongo_query = {}
        
        for field, conditions in query.filters.items():
            field_query = {}
            
            for operator, value in conditions.items():
                if operator == QueryOperator.EQ:
                    field_query = value
                else:
                    field_query[f"${operator}"] = value
            
            mongo_query[field] = field_query if len(field_query) > 1 else field_query
        
        return mongo_query

# Global storage engine instances
kundli_storage = StorageEngine(
    StorageConfig(
        type=StorageType.MONGODB,
        connection_string="mongodb://localhost:27017",
        database_name="kundli_db",
        collection_name="kundli_data"
    )
)

pattern_storage = StorageEngine(
    StorageConfig(
        type=StorageType.MONGODB,
        connection_string="mongodb://localhost:27017",
        database_name="kundli_db",
        collection_name="pattern_data"
    )
)
