from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from app.db.mongodb import MongoDB
from app.models.user import UserInDB, UserCreate, UserUpdate

class UserRepository:
    collection = MongoDB.db.users

    @classmethod
    async def create_user(cls, user: UserCreate) -> UserInDB:
        user_dict = user.dict()
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = user_dict["created_at"]
        result = await cls.collection.insert_one(user_dict)
        return await cls.get_user_by_id(str(result.inserted_id))

    @classmethod
    async def get_user_by_id(cls, user_id: str) -> Optional[UserInDB]:
        user = await cls.collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["id"] = str(user.pop("_id"))
            return UserInDB(**user)
        return None

    @classmethod
    async def get_user_by_email(cls, email: str) -> Optional[UserInDB]:
        user = await cls.collection.find_one({"email": email})
        if user:
            user["id"] = str(user.pop("_id"))
            return UserInDB(**user)
        return None

    @classmethod
    async def get_user_by_username(cls, username: str) -> Optional[UserInDB]:
        user = await cls.collection.find_one({"username": username})
        if user:
            user["id"] = str(user.pop("_id"))
            return UserInDB(**user)
        return None

    @classmethod
    async def update_user(cls, user_id: str, update_data: UserUpdate) -> Optional[UserInDB]:
        update_dict = update_data.dict(exclude_unset=True)
        update_dict["updated_at"] = datetime.utcnow()

        result = await cls.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_dict}
        )

        if result.modified_count:
            return await cls.get_user_by_id(user_id)
        return None

    @classmethod
    async def delete_user(cls, user_id: str) -> bool:
        result = await cls.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

    @classmethod
    async def list_users(
        cls, skip: int = 0, limit: int = 10, role: Optional[str] = None
    ) -> List[UserInDB]:
        query = {"role": role} if role else {}
        cursor = cls.collection.find(query)
        cursor.skip(skip).limit(limit).sort("created_at", -1)
        users = []
        async for user in cursor:
            user["id"] = str(user.pop("_id"))
            users.append(UserInDB(**user))
        return users

    @classmethod
    async def update_last_login(cls, user_id: str) -> None:
        await cls.collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "last_login": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }
            }
        )

    @classmethod
    async def add_saved_kundli(cls, user_id: str, kundli_id: str) -> bool:
        result = await cls.collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$addToSet": {"saved_kundlis": kundli_id},
                "$set": {"updated_at": datetime.utcnow()},
            }
        )
        return result.modified_count > 0

    @classmethod
    async def remove_saved_kundli(cls, user_id: str, kundli_id: str) -> bool:
        result = await cls.collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$pull": {"saved_kundlis": kundli_id},
                "$set": {"updated_at": datetime.utcnow()},
            }
        )
        return result.modified_count > 0
