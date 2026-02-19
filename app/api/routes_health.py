from fastapi import APIRouter
from app.storage.in_memory_store import store

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/ready")
async def readiness_check():
    readiness = store.is_ready()
    return readiness
