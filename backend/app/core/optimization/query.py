"""
Query Optimization Module
PGF Protocol: QUERY_001
Gate: GATE_4
Version: 1.0.0
"""

from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
import logging
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING, IndexModel
from .profiler import database_profiler

# Configure logging
logger = logging.getLogger(__name__)

class QueryOptimizer:
    """MongoDB query optimization utilities"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.indexes_created = False
    
    async def ensure_indexes(self):
        """Create necessary indexes"""
        if self.indexes_created:
            return
        
        try:
            # Kundli collection indexes
            kundli_indexes = [
                IndexModel([("user_id", ASCENDING)]),
                IndexModel([("created_at", DESCENDING)]),
                IndexModel([
                    ("date", ASCENDING),
                    ("time", ASCENDING),
                    ("latitude", ASCENDING),
                    ("longitude", ASCENDING)
                ]),
                IndexModel([("calculation_type", ASCENDING)])
            ]
            await self.db.kundlis.create_indexes(kundli_indexes)
            
            # User collection indexes
            user_indexes = [
                IndexModel([("email", ASCENDING)], unique=True),
                IndexModel([("username", ASCENDING)], unique=True),
                IndexModel([("last_login", DESCENDING)])
            ]
            await self.db.users.create_indexes(user_indexes)
            
            # Calculation collection indexes
            calc_indexes = [
                IndexModel([("kundli_id", ASCENDING)]),
                IndexModel([("type", ASCENDING)]),
                IndexModel([("created_at", DESCENDING)])
            ]
            await self.db.calculations.create_indexes(calc_indexes)
            
            self.indexes_created = True
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.error(f"Error creating indexes: {str(e)}")
            raise
    
    @database_profiler.profile_query("find_kundli")
    async def find_kundli(
        self,
        query: Dict[str, Any],
        projection: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Optimized kundli query"""
        try:
            result = await self.db.kundlis.find_one(
                query,
                projection=projection
            )
            return result
        except Exception as e:
            logger.error(f"Error finding kundli: {str(e)}")
            return None
    
    @database_profiler.profile_query("find_kundlis")
    async def find_kundlis(
        self,
        query: Dict[str, Any],
        projection: Optional[Dict[str, Any]] = None,
        sort: Optional[List[tuple]] = None,
        limit: int = 10,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """Optimized kundlis query with pagination"""
        try:
            cursor = self.db.kundlis.find(
                query,
                projection=projection
            )
            
            if sort:
                cursor = cursor.sort(sort)
            
            cursor = cursor.skip(skip).limit(limit)
            
            return await cursor.to_list(length=None)
        except Exception as e:
            logger.error(f"Error finding kundlis: {str(e)}")
            return []
    
    @database_profiler.profile_query("aggregate_kundlis")
    async def aggregate_kundlis(
        self,
        pipeline: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Optimized aggregation query"""
        try:
            cursor = self.db.kundlis.aggregate(pipeline)
            return await cursor.to_list(length=None)
        except Exception as e:
            logger.error(f"Error aggregating kundlis: {str(e)}")
            return []
    
    @database_profiler.profile_query("update_kundli")
    async def update_kundli(
        self,
        query: Dict[str, Any],
        update: Dict[str, Any],
        upsert: bool = False
    ) -> bool:
        """Optimized update query"""
        try:
            result = await self.db.kundlis.update_one(
                query,
                update,
                upsert=upsert
            )
            return result.modified_count > 0 or (upsert and result.upserted_id)
        except Exception as e:
            logger.error(f"Error updating kundli: {str(e)}")
            return False
    
    @database_profiler.profile_query("bulk_update_kundlis")
    async def bulk_update_kundlis(
        self,
        operations: List[Dict[str, Any]]
    ) -> bool:
        """Optimized bulk update"""
        try:
            result = await self.db.kundlis.bulk_write(operations)
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error bulk updating kundlis: {str(e)}")
            return False
    
    async def optimize_query(
        self,
        query: Dict[str, Any],
        collection: str
    ) -> Dict[str, Any]:
        """Optimize query based on indexes and data distribution"""
        optimized = query.copy()
        
        try:
            # Get collection stats
            stats = await self.db.command({
                "collStats": collection,
                "scale": 1024
            })
            
            # Check if query uses indexes
            explain = await self.db[collection].find(
                optimized
            ).explain()
            
            # If not using indexes and collection is large,
            # try to optimize
            if (
                stats.get("size", 0) > 100 * 1024 * 1024 and  # 100MB
                explain.get("queryPlanner", {}).get("winningPlan", {}).get("stage") == "COLLSCAN"
            ):
                # Add index hints based on available indexes
                indexes = await self.db[collection].index_information()
                for index_name, index_info in indexes.items():
                    if index_name != "_id_":
                        fields = [field[0] for field in index_info["key"]]
                        if any(field in optimized for field in fields):
                            optimized["$hint"] = index_name
                            break
            
            return optimized
            
        except Exception as e:
            logger.error(f"Error optimizing query: {str(e)}")
            return query

# Example query patterns
QUERY_PATTERNS = {
    "recent_kundlis": {
        "query": {
            "user_id": "$user_id",
            "created_at": {
                "$gte": "$start_date"
            }
        },
        "sort": [("created_at", -1)],
        "projection": {
            "_id": 1,
            "date": 1,
            "time": 1,
            "calculation_type": 1
        }
    },
    "user_calculations": {
        "pipeline": [
            {
                "$match": {
                    "user_id": "$user_id"
                }
            },
            {
                "$group": {
                    "_id": "$calculation_type",
                    "count": {"$sum": 1},
                    "last_calculation": {"$max": "$created_at"}
                }
            }
        ]
    }
}

# Usage examples:
"""
# Initialize optimizer
db = AsyncIOMotorDatabase(client, "kundli_db")
optimizer = QueryOptimizer(db)

# Ensure indexes
await optimizer.ensure_indexes()

# Find recent kundlis
pattern = QUERY_PATTERNS["recent_kundlis"]
query = pattern["query"].copy()
query["user_id"] = user_id
query["created_at"]["$gte"] = datetime.utcnow() - timedelta(days=7)

results = await optimizer.find_kundlis(
    query=query,
    projection=pattern["projection"],
    sort=pattern["sort"]
)

# Aggregate user calculations
pattern = QUERY_PATTERNS["user_calculations"]
pipeline = pattern["pipeline"].copy()
pipeline[0]["$match"]["user_id"] = user_id

results = await optimizer.aggregate_kundlis(pipeline)
"""
