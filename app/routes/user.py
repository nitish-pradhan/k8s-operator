from fastapi import APIRouter, Depends

from app.models.user import User
from app.config.db import collection
from app.schemas.user import serializeDict, serializeList
from bson import ObjectId

from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from app.auth.schemas import UserAuth, TokenSchema
from app.auth.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)
from app.auth.deps import get_current_user

user = APIRouter()


@user.get('/me', summary='Get details of currently logged in user', response_model=dict)
async def get_me(user: User = Depends(get_current_user)):
    return {'name': user['name'], 'email': user['email']}


@user.get("/users/", response_model=list[User], dependencies=[Depends(get_current_user)])
async def find_all_users(page: int = 0, limit: int = 10):
    users = collection.find().skip((page-1) * limit).limit(limit)
    return serializeList(users)


@user.get("/users/{id}", response_model=User, dependencies=[Depends(get_current_user)])
async def find_one_user(name: str):
    user = collection.find_one({"name": name})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user.post("/users/", response_model=User, dependencies=[Depends(get_current_user)])
async def create_user(user: User):
    inserted_item = collection.insert_one(dict(user))
    return {"id": str(inserted_item.inserted_id), **user.dict()}

@user.put("/users/{id}", response_model=User, dependencies=[Depends(get_current_user)])
async def update_user(id: str, user: User):
    existing_user = collection.find_one({"_id":ObjectId(id)})
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    collection.find_one_and_update({"_id":ObjectId(id)}, {"$set": dict(user)})
    return serializeDict(collection.find_one({"_id":ObjectId(id)}))

@user.delete("/users/{id}", response_model=dict, dependencies=[Depends(get_current_user)])
async def delete_user(id: str):
    deletion_result = collection.delete_one({"_id": ObjectId(id)})
    if deletion_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "message": "User deleted"}


@user.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')

@user.post('/signup', summary="Create new user", response_model=User, dependencies=[Depends(get_current_user)])
async def create_user(user: User):
    # querying database to check if user already exist
    check = collection.find_one({"email": user.email})
    if check is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    user.password = get_hashed_password(user.password)
    inserted_item = collection.insert_one(dict(user))
    return {"id": str(inserted_item.inserted_id), **user.dict()}


@user.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = collection.find_one({"name": form_data.username})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    hashed_password = user['password']
    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }