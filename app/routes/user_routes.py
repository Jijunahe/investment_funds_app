# app/routes/user_routes.py

from fastapi import APIRouter, HTTPException,Depends
from app.models.user import User
from app.models.usuarios_response import UsuariosResponseAll

from app.database.db import get_db
from bson.objectid import ObjectId
from typing import List

router = APIRouter()

@router.post("/users/", response_model=User)
async def create_user(user: User):
    db = get_db()
    user_dict = user.dict()
    user_dict['_id'] = ObjectId()  # Usar ObjectId para MongoDB
    db.users.insert_one(user_dict)
    return user


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    db = get_db()
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user['id'] = user_id   
    return user

@router.get("/users/", response_model=List[UsuariosResponseAll])
async def get_userAll(db = Depends(get_db)) -> List[UsuariosResponseAll]:
    db = get_db()
    userAll = db.users.find()
    if not userAll:
        raise HTTPException(status_code=404, detail="No hay usuarios")
    
    
    users = []
    for user in userAll:
        users.append(UsuariosResponseAll.from_mongo(user))
  
    return users 


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: User):
    db = get_db()
    updated_user = db.users.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": user.dict()},
        return_document=True
    )
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user['_id'] = str(updated_user['_id'])  # Convertir ObjectId a string
    return updated_user

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    db = get_db()
    result = db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
