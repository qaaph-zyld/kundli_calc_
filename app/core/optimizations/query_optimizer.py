"""
Query Optimization Module
PGF Protocol: OPT_001
Gate: GATE_5
Version: 1.0.0
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING, IndexModel

logger = logging.getLogger(__name__)

class QueryOptimizer:
    """Optimizer for MongoDB queries in the Kundli service."""
    
    def __init__(self, db: AsyncIOMotorClient):
        """Initialize query optimizer."""
        self.db = db
        self.collection_stats = {}
        self.query_patterns = {}
    
    async def create_indexes(self):
        """Create optimized indexes based on common query patterns."""
        # Kundli collection indexes
        kundli_indexes = [
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("created_at", DESCENDING)]),
            IndexModel([
                ("birth_details.date", ASCENDING),
                ("birth_details.time", ASCENDING)
            ]),
            IndexModel([
                ("birth_details.latitude", ASCENDING),
                ("birth_details.longitude", ASCENDING)
            ]),
            IndexModel([("planets.Sun", ASCENDING)]),
            IndexModel([("planets.Moon", ASCENDING)]),
            IndexModel([("planets.Ascendant", ASCENDING)])
        ]
        
        # User collection indexes
        user_indexes = [
            IndexModel([("email", ASCENDING), ("is_active", ASCENDING)]),
            IndexModel([("last_login", DESCENDING)]),
            IndexModel([("subscription.status", ASCENDING)])
        ]
        
        # Create indexes
        await self.db.kundlis.create_indexes(kundli_indexes)
        await self.db.users.create_indexes(user_indexes)
        
        logger.info("Created optimized indexes for collections")
    
    async def analyze_query_patterns(self):
        """Analyze and optimize common query patterns."""
        # Get system.profile data
        pipeline = [
            {"$group": {
                "_id": "$query_pattern",
                "count": {"$sum": 1},
                "avg_execution_time": {"$avg": "$millis"}
            }},
            {"$sort": {"count": -1}}
        ]
        
        patterns = await self.db.system.profile.aggregate(pipeline).to_list(None)
        self.query_patterns = {p["_id"]: p for p in patterns}
        
        logger.info(f"Analyzed {len(patterns)} query patterns")
        return patterns
    
    def optimize_query(self, query: Dict) -> Dict:
        """Optimize a query based on analysis."""
        optimized = query.copy()
        
        # Add index hints based on query pattern
        if "user_id" in query:
            optimized["$hint"] = {"user_id": 1}
        
        # Add query planner directives
        if "birth_details.date" in query and "birth_details.time" in query:
            optimized["$hint"] = {
                "birth_details.date": 1,
                "birth_details.time": 1
            }
        
        # Add projection optimization
        if "projection" not in optimized:
            optimized["projection"] = {
                "_id": 1,
                "birth_details": 1,
                "planets": 1
            }
        
        return optimized
    
    async def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics for optimization."""
        collections = ["kundlis", "users", "calculations"]
        stats = {}
        
        for collection in collections:
            stats[collection] = await self.db.command("collStats", collection)
        
        self.collection_stats = stats
        return stats
    
    def suggest_optimizations(self) -> List[Dict]:
        """Suggest query optimizations based on analysis."""
        suggestions = []
        
        # Check for missing indexes
        for pattern, stats in self.query_patterns.items():
            if stats["avg_execution_time"] > 100:  # ms
                suggestions.append({
                    "type": "index",
                    "pattern": pattern,
                    "reason": "High execution time",
                    "suggestion": "Create index for pattern"
                })
        
        # Check collection sizes
        for coll, stats in self.collection_stats.items():
            if stats.get("size", 0) > 1_000_000_000:  # 1GB
                suggestions.append({
                    "type": "sharding",
                    "collection": coll,
                    "reason": "Large collection size",
                    "suggestion": "Consider sharding"
                })
        
        return suggestions
    
    async def optimize_aggregation_pipeline(
        self,
        pipeline: List[Dict]
    ) -> List[Dict]:
        """Optimize MongoDB aggregation pipeline."""
        optimized = []
        
        for stage in pipeline:
            # Optimize $match stages
            if "$match" in stage:
                stage["$match"] = self.optimize_query(stage["$match"])
            
            # Optimize $sort stages
            if "$sort" in stage and len(optimized) > 0:
                # Try to move $sort before $project if possible
                prev_stage = optimized[-1]
                if "$project" in prev_stage:
                    optimized[-1] = stage
                    optimized.append(prev_stage)
                    continue
            
            # Add memory limits to $group stages
            if "$group" in stage:
                stage["allowDiskUse"] = True
            
            optimized.append(stage)
        
        return optimized
    
    async def create_partial_indexes(self):
        """Create partial indexes for specific query patterns."""
        # Partial index for active users
        await self.db.users.create_index(
            [("email", ASCENDING)],
            partialFilterExpression={"is_active": True}
        )
        
        # Partial index for premium kundlis
        await self.db.kundlis.create_index(
            [("created_at", DESCENDING)],
            partialFilterExpression={"is_premium": True}
        )
        
        logger.info("Created partial indexes for optimized queries")
    
    async def optimize_text_search(self):
        """Optimize text search capabilities."""
        # Create text indexes
        await self.db.kundlis.create_index([
            ("notes", "text"),
            ("tags", "text")
        ])
        
        # Create compound text index
        await self.db.calculations.create_index([
            ("description", "text"),
            ("results", "text")
        ])
        
        logger.info("Optimized text search indexes")
    
    def get_query_plan(self, query: Dict) -> Dict:
        """Get execution plan for a query."""
        return {
            "original": query,
            "optimized": self.optimize_query(query),
            "indexes_used": self._get_used_indexes(query),
            "estimated_cost": self._estimate_query_cost(query)
        }
    
    def _get_used_indexes(self, query: Dict) -> List[str]:
        """Get list of indexes used by a query."""
        indexes = []
        
        for field in query.keys():
            if field in ["user_id", "created_at"]:
                indexes.append(f"{field}_1")
            elif field.startswith("birth_details."):
                indexes.append("birth_details_compound")
            elif field.startswith("planets."):
                indexes.append(f"planets_{field.split('.')[1]}_1")
        
        return indexes
    
    def _estimate_query_cost(self, query: Dict) -> Dict:
        """Estimate the cost of a query."""
        return {
            "docs_examined": self._estimate_docs_examined(query),
            "index_keys_examined": len(self._get_used_indexes(query)),
            "in_memory": self._will_use_memory(query)
        }
    
    def _estimate_docs_examined(self, query: Dict) -> int:
        """Estimate number of documents examined."""
        # Simple estimation based on query complexity
        base = 100
        for key in query.keys():
            if key in self.collection_stats.get("kundlis", {}).get("count", 0):
                base *= 0.1
        return int(base)
    
    def _will_use_memory(self, query: Dict) -> bool:
        """Determine if query will use in-memory sorting."""
        return "$sort" in query and len(query.get("$sort", {})) > 2
