from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING, TEXT, DESCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import Optional
from app.core.config import settings
import logging
import asyncio

logger = logging.getLogger(__name__)

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    db = None
    _max_retries = 3
    _retry_delay = 5  # seconds

    @classmethod
    async def connect_to_database(cls):
        """Connect to MongoDB with retries."""
        for attempt in range(cls._max_retries):
            try:
                cls.client = AsyncIOMotorClient(
                    settings.MONGODB_URL,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=5000,
                )
                # Verify connection is successful
                await cls.client.admin.command('ping')
                
                cls.db = cls.client[settings.MONGODB_DB_NAME]
                await cls.create_indexes()
                logger.info("Successfully connected to MongoDB.")
                return
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                if attempt == cls._max_retries - 1:
                    logger.error(f"Failed to connect to MongoDB after {cls._max_retries} attempts: {str(e)}")
                    raise
                logger.warning(f"Failed to connect to MongoDB (attempt {attempt + 1}/{cls._max_retries}). Retrying in {cls._retry_delay} seconds...")
                await asyncio.sleep(cls._retry_delay)

    @classmethod
    async def close_database_connection(cls):
        """Close MongoDB connection safely."""
        if cls.client:
            try:
                cls.client.close()
                logger.info("Closed MongoDB connection.")
            except Exception as e:
                logger.error(f"Error closing MongoDB connection: {str(e)}")

    @classmethod
    async def create_indexes(cls):
        """Create all required indexes."""
        try:
            # User indexes
            await cls.db.users.create_indexes([
                IndexModel([("email", ASCENDING)], unique=True),
                IndexModel([("username", ASCENDING)], unique=True),
                IndexModel([("email", TEXT), ("username", TEXT)]),
                IndexModel([("role", ASCENDING)]),
                IndexModel([("is_active", ASCENDING)]),
                IndexModel([("last_login", DESCENDING)]),
            ])

            # Kundli indexes
            await cls.db.kundlis.create_indexes([
                IndexModel([("user_id", ASCENDING)]),
                IndexModel([("created_at", DESCENDING)]),
                IndexModel([("request.date", ASCENDING)]),
                IndexModel([("request.latitude", ASCENDING)]),
                IndexModel([("request.longitude", ASCENDING)]),
                IndexModel([("request.timezone", ASCENDING)]),
            ])

            # Predictions indexes
            await cls.db.predictions.create_indexes([
                IndexModel([("kundli_id", ASCENDING)]),
                IndexModel([("generated_at", DESCENDING)]),
                IndexModel([("type", ASCENDING)]),
            ])

            # Matching indexes
            await cls.db.matching.create_indexes([
                IndexModel([("kundli1_id", ASCENDING)]),
                IndexModel([("kundli2_id", ASCENDING)]),
                IndexModel([("total_score", DESCENDING)]),
                IndexModel([("generated_at", DESCENDING)]),
            ])

            # Transit indexes
            await cls.db.transits.create_indexes([
                IndexModel([("birth_kundli_id", ASCENDING)]),
                IndexModel([("transit_date", ASCENDING)]),
                IndexModel([("generated_at", DESCENDING)]),
            ])

            logger.info("Successfully created MongoDB indexes.")
        except Exception as e:
            logger.error(f"Failed to create MongoDB indexes: {str(e)}")
            raise

    @classmethod
    async def get_collection(cls, collection_name: str):
        """Get a collection with connection check."""
        if not cls.client:
            await cls.connect_to_database()
        return cls.db[collection_name]

    @classmethod
    async def ping(cls) -> bool:
        """Check if MongoDB connection is alive."""
        try:
            await cls.client.admin.command('ping')
            return True
        except Exception:
            return False
