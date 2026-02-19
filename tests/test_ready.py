import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.storage.in_memory_store import store

client = TestClient(app)

def teardown_function():
    store.__init__()

def test_readiness_flow():
    # Initially not ready
    response = client.get("/ready")
    assert response.json()["ready"] is False
    
    # Ingest enough points for all symbols
    headers = {"X-API-Key": settings.APP_API_KEY}
    bars = []
    
    # Create valid payload for all allowed symbols
    # Create valid payload for all allowed symbols
    import datetime
    base_time = datetime.datetime(2023, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
    
    for symbol in settings.ALLOWED_SYMBOLS:
        # Generate MIN_POINTS_READY bars
        for i in range(settings.MIN_POINTS_READY):
            ts = base_time + datetime.timedelta(seconds=i)
            bars.append({
                "symbol": symbol,
                "ts": ts.isoformat(),
                "open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0
            })
            
    # Send in batches to avoid huge payload if needed, 
    # but for test logic one batch is fine if not too huge.
    # 8 symbols * 300 points = 2400 bars. Reasonable.
    
    # However, to be safe and simulating batches:
    chunk_size = 500
    for i in range(0, len(bars), chunk_size):
        chunk = bars[i:i+chunk_size]
        client.post("/ingest", json={"bars": chunk}, headers=headers)
        
    # Check readiness
    response = client.get("/ready")
    data = response.json()
    assert data["ready"] is True
