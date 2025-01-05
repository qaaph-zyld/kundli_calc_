from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from app.db.mongodb import MongoDB
from app.models.kundli import (
    KundliRequest,
    KundliResponse,
    KundliPredictions,
    TransitRequest,
    TransitResponse,
    MatchingRequest,
    MatchingResponse,
)

class KundliRepository:
    collection = MongoDB.db.kundlis
    predictions_collection = MongoDB.db.predictions
    transits_collection = MongoDB.db.transits
    matching_collection = MongoDB.db.matching

    @classmethod
    async def create_kundli(cls, user_id: str, request: KundliRequest) -> KundliResponse:
        kundli_dict = request.dict()
        kundli_dict.update({
            "user_id": user_id,
            "created_at": datetime.utcnow(),
        })
        result = await cls.collection.insert_one(kundli_dict)
        return await cls.get_kundli(str(result.inserted_id))

    @classmethod
    async def get_kundli(cls, kundli_id: str) -> Optional[KundliResponse]:
        kundli = await cls.collection.find_one({"_id": ObjectId(kundli_id)})
        if kundli:
            kundli["id"] = str(kundli.pop("_id"))
            return KundliResponse(**kundli)
        return None

    @classmethod
    async def list_user_kundlis(
        cls, user_id: str, skip: int = 0, limit: int = 10
    ) -> List[KundliResponse]:
        cursor = cls.collection.find({"user_id": user_id})
        cursor.skip(skip).limit(limit).sort("created_at", -1)
        kundlis = []
        async for kundli in cursor:
            kundli["id"] = str(kundli.pop("_id"))
            kundlis.append(KundliResponse(**kundli))
        return kundlis

    @classmethod
    async def save_predictions(
        cls, kundli_id: str, predictions: KundliPredictions
    ) -> KundliPredictions:
        predictions_dict = predictions.dict()
        predictions_dict["kundli_id"] = kundli_id
        result = await cls.predictions_collection.insert_one(predictions_dict)
        return await cls.get_predictions(str(result.inserted_id))

    @classmethod
    async def get_predictions(cls, prediction_id: str) -> Optional[KundliPredictions]:
        prediction = await cls.predictions_collection.find_one(
            {"_id": ObjectId(prediction_id)}
        )
        if prediction:
            prediction["id"] = str(prediction.pop("_id"))
            return KundliPredictions(**prediction)
        return None

    @classmethod
    async def save_transit(
        cls, request: TransitRequest, response: TransitResponse
    ) -> TransitResponse:
        transit_dict = {
            "request": request.dict(),
            "response": response.dict(),
            "created_at": datetime.utcnow(),
        }
        result = await cls.transits_collection.insert_one(transit_dict)
        return await cls.get_transit(str(result.inserted_id))

    @classmethod
    async def get_transit(cls, transit_id: str) -> Optional[TransitResponse]:
        transit = await cls.transits_collection.find_one({"_id": ObjectId(transit_id)})
        if transit:
            transit["id"] = str(transit.pop("_id"))
            return TransitResponse(**transit["response"])
        return None

    @classmethod
    async def save_matching(
        cls, request: MatchingRequest, response: MatchingResponse
    ) -> MatchingResponse:
        matching_dict = {
            "request": request.dict(),
            "response": response.dict(),
            "created_at": datetime.utcnow(),
        }
        result = await cls.matching_collection.insert_one(matching_dict)
        return await cls.get_matching(str(result.inserted_id))

    @classmethod
    async def get_matching(cls, matching_id: str) -> Optional[MatchingResponse]:
        matching = await cls.matching_collection.find_one(
            {"_id": ObjectId(matching_id)}
        )
        if matching:
            matching["id"] = str(matching.pop("_id"))
            return MatchingResponse(**matching["response"])
        return None
