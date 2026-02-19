from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, root_validator
import pandas as pd
from app.core.security import validate_api_key
from app.storage.in_memory_store import store, InMemoryStore
from app.core.config import settings

router = APIRouter()

class Bar(BaseModel):
    symbol: str
    ts: str  # ISO timestamp
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = 0.0

class IngestRequest(BaseModel):
    source: Optional[str] = None
    bars: List[Bar]

@router.post("/ingest", dependencies=[Depends(validate_api_key)])
async def ingest_bars(payload: IngestRequest):
    if not payload.bars:
        return {"status": "ok", "ingested": 0}

    # Helper: Check if allowed symbol
    # We could filter out bad symbols or raise error. 
    # Let's filter to be robust.
    valid_bars = [b for b in payload.bars if b.symbol in settings.ALLOWED_SYMBOLS]
    
    if not valid_bars:
         return {"status": "ok", "ingested": 0, "ignored": len(payload.bars)}

    # Convert to DataFrame
    # List of dicts
    data = [b.model_dump() for b in valid_bars]
    df = pd.DataFrame(data)
    
    # Process per symbol
    ingested_counts = {}
    
    # Metrics: Batch Counter
    from app.observability.prometheus import (
        INGEST_BATCHES_TOTAL, 
        INGEST_ROWS_TOTAL, 
        INGEST_PROCESSING_SECONDS,
        STORE_POINTS,
        STORE_SYMBOLS_TOTAL
    )
    import time
    
    start_time = time.time()
    INGEST_BATCHES_TOTAL.inc()
    
    for symbol, group in df.groupby("symbol"):
        # group is a DataFrame
        count = len(group)
        
        # Pass to store
        store.append_bars(symbol, group)
        ingested_counts[symbol] = count
        
        # Metrics: Rows per symbol
        INGEST_ROWS_TOTAL.labels(symbol=symbol).inc(count)
        
        # Metrics: Update Gauge for stored points
        current_count = len(store.store[symbol])
        STORE_POINTS.labels(symbol=symbol).set(current_count)

    # Metrics: Duration
    INGEST_PROCESSING_SECONDS.observe(time.time() - start_time)
    
    # Metrics: Total Symbols Gauge
    STORE_SYMBOLS_TOTAL.set(len(store.store))

    return {
        "status": "ok",
        "ingested": len(valid_bars),
        "per_symbol": ingested_counts,
        "ignored": len(payload.bars) - len(valid_bars)
    }
