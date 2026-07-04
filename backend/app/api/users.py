from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.database import get_db, get_tenant_slug
from typing import List, Optional
import uuid
import time

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
    username: str
    email: str
    role: str = "Viewer"

@router.get("")
async def list_users():
    """Lists users belonging to the active organization."""
    slug = get_tenant_slug()
    db = get_db()
    
    cursor = db.users.find({"tenant_id": slug}).sort("created_at", -1)
    users = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        users.append(doc)
    return users

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate):
    """Creates a user record mapped to the current tenant."""
    slug = get_tenant_slug()
    db = get_db()
    
    existing = await db.users.find_one({"email": payload.email, "tenant_id": slug})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists in the organization."
        )
        
    user_doc = {
        "user_id": str(uuid.uuid4()),
        "tenant_id": slug,
        "username": payload.username,
        "email": payload.email,
        "role": payload.role,
        "created_at": time.time(),
        "updated_at": time.time()
    }
    
    result = await db.users.insert_one(user_doc)
    user_doc["_id"] = str(result.inserted_id)
    return user_doc
