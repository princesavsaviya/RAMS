import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.storage.in_memory_store import store
import pandas as pd

client = TestClient(app)

def teardown_module(module):
    # Reset store
    store.__init__()

def test_ingest_no_auth():
    response = client.post("/ingest", json={"bars": []})
    assert response.status_code == 401

def test_ingest_valid():
    headers = {"X-API-Key": settings.APP_API_KEY}
    payload = {
        "bars": [
            {
                "symbol": "EURUSD",
                "ts": "2023-10-27T10:00:00Z",
                "open": 1.05,
                "high": 1.06,
                "low": 1.04,
                "close": 1.055
            }
        ]
    }
    response = client.post("/ingest", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["ingested"] == 1
    assert data["per_symbol"]["EURUSD"] == 1

def test_ingest_out_of_order():
    store.__init__() # Reset
    headers = {"X-API-Key": settings.APP_API_KEY}
    payload = {
        "bars": [
            {
                "symbol": "EURUSD",
                "ts": "2023-10-27T10:00:02Z",
                "open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0
            },
            {
                "symbol": "EURUSD",
                "ts": "2023-10-27T10:00:01Z",
                "open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0
            }
        ]
    }
    client.post("/ingest", json=payload, headers=headers)
    
    df = store.get_symbol_df("EURUSD")
    # Verify sorted
    assert df.iloc[0]["ts"] < df.iloc[1]["ts"]
