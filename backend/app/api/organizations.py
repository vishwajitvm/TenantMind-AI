from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.database import get_mongo_client
import time

router = APIRouter(prefix="/organizations", tags=["Organizations"])

class OrganizationCreate(BaseModel):
    name: str
    slug: str

@router.get("")
async def list_organizations():
    """Lists all organizations in the platform database."""
    client = get_mongo_client()
    db = client["platform_db"]
    cursor = db.organizations.find().sort("created_at", -1)
    orgs = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        orgs.append(doc)
    return orgs

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_organization(payload: OrganizationCreate):
    """Creates a new organization in the platform database."""
    client = get_mongo_client()
    db = client["platform_db"]
    
    # Check if slug already exists
    existing = await db.organizations.find_one({"slug": payload.slug})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Organization with slug '{payload.slug}' already exists."
        )
        
    org_doc = {
        "name": payload.name,
        "slug": payload.slug,
        "created_at": time.time(),
        "updated_at": time.time()
    }
    
    result = await db.organizations.insert_one(org_doc)
    org_doc["_id"] = str(result.inserted_id)
    return org_doc
