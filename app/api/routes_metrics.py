from fastapi import APIRouter
from app.storage.in_memory_store import store

router = APIRouter()

@router.get("/store/stats")
async def get_store_stats():
    return store.stats()
