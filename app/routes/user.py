from fastapi import APIRouter, HTTPException

from app.models.user import User
from app.config.db import collection
from app.schemas.user import serializeDict, serializeList
from bson import ObjectId
user = APIRouter()


@user.get("/users/", response_model=list[User])
async def find_all_users(skip: int = 0, limit: int = 10):
    users = collection.find().skip(skip).limit(limit)
    #return list(users)
    return serializeList(users)

@user.get("/users/{id}", response_model=User)
async def find_one_user(id: str):
    user = collection.find_one({"_id":ObjectId(id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user.post("/users/", response_model=User)
async def create_user(user: User):
    inserted_item = collection.insert_one(dict(user))
    return {"id": str(inserted_item.inserted_id), **user.dict()}

@user.put("/users/{id}", response_model=User)
async def update_user(id: str, user: User):
    existing_user = collection.find_one({"_id":ObjectId(id)})
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    collection.find_one_and_update({"_id":ObjectId(id)}, {"$set": dict(user)})
    return serializeDict(collection.find_one({"_id":ObjectId(id)}))

@user.delete("/users/{id}", response_model=dict)
async def delete_user(id: str):
    deletion_result = collection.delete_one({"_id": ObjectId(id)})
    if deletion_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "message": "User deleted"}