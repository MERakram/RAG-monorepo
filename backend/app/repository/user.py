from datetime import datetime, timezone
from pymongo import MongoClient
import pymongo
from typing import Optional
from app.core.config import MONGO_COLLECTION_USERS
from app.repository.base import BaseRepository
from app.model.user import UserDB
from pydantic import conint
from app.schema.user import User
from fastapi.encoders import jsonable_encoder


class UserRepository(BaseRepository):
    """
    Repository class for interacting with the users collection in MongoDB.

    This class provides methods for creating, retrieving, updating, and deleting user data in the MongoDB database.
    """


    def __init__(self, mongo: MongoClient):
        """
        Initializes the UserRepository with the MongoDB client.

        Args:
            mongo (MongoClient): The MongoDB client instance.
        """
        self._mongo = mongo
        super().__init__(mongo)

    def create(self, model: UserDB, collection: MONGO_COLLECTION_USERS) -> User:
        model_in_json = jsonable_encoder(model)
        new_model = self.database[collection].insert_one(document=model_in_json)
        created_model = self.database[collection].find_one(
            {"_id": new_model.inserted_id}

        )
        return UserDB(**created_model)
    
    def get_by_id(self, collection: MONGO_COLLECTION_USERS, id: str) -> User :
        find_model = self.database[collection].find_one(
            {"_id": id}
        )

        return UserDB(**find_model)

    def get_by_name(self, collection: MONGO_COLLECTION_USERS, name: str):
        find_model = self.database[collection].find_one(
            {"username": name}
        )

        return UserDB(**find_model) if find_model else None

    def get_list(self,
                 collection: MONGO_COLLECTION_USERS,
                 sort_field: str = "created_at",
                 sort_order: int = pymongo.DESCENDING,
                 skip: conint(ge=0) = 0,
                 limit: conint(ge=5, multiple_of=5) = 10
                 ):

        users= self.database[collection].find({}).sort([(sort_field, sort_order)]).skip(skip).limit(limit)
        total = self.database[collection].count_documents(filter={})

        return [UserDB(**user) for user in users], total

    def delete(self, collection: MONGO_COLLECTION_USERS, id: str) -> User:
        find_model = self.database[collection].find_one(
            {"_id": id}
        )
        delete_model = self.database[collection].delete_one(
            {"_id": id}
        )

        return UserDB(**find_model)

    def update(self,
               collection: MONGO_COLLECTION_USERS,
               id: str,
               req):


        request_in_json = jsonable_encoder(req)
        print(request_in_json)

        def remove_pairs_with_none_in_place(d):
            pairs_with_none = {k: v for k, v in d.items() if v is None}
            for key in pairs_with_none.keys():
                del d[key]
            return pairs_with_none

        if req == None:
            updated_model = self.database[collection].find_one({"_id": id})
            return User(**updated_model)

        else:
            remove_pairs_with_none_in_place(request_in_json)
            update_model = self.database[collection].update_one(filter={'_id': id}, update={"$set": request_in_json})
            updated_model = self.database[collection].find_one({"_id": id})
            return UserDB(**updated_model)


    def activate_user(self, collection: str, user_id: str) -> Optional[UserDB]:
        user_document = self.database[collection].find_one({"_id": user_id})
        
        if not user_document:
            return None 

        is_correct_type = user_document.get("role") == 'agent'
        is_currently_inactive = user_document.get("active") is False

        if not (is_correct_type and is_currently_inactive):
            return None 

        update_payload = {
            "active": True,
            "updated_at": datetime.now(timezone.utc), 
        }
        
        self.database[collection].update_one(
            filter={"_id": user_id},
            update={"$set": update_payload}
        )
        
        updated_user_document = self.database[collection].find_one({"_id": user_id})
        
        if updated_user_document and updated_user_document.get("active") is True:
            return UserDB(**updated_user_document)
        
        return None

    def get_by_email(self, collection: MONGO_COLLECTION_USERS, email: str):
        find_model = self.database[collection].find_one(
            {"email": email}
        )

        return UserDB(**find_model) if find_model else None