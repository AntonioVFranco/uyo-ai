import datetime as dt
import pytest
from fastapi.testclient import TestClient

from apps.uyo_ai_api.app import app


def test_ohlcv_daily_last_7_days() -> None:
    client = TestClient(app)
    end = dt.date.today()
    start = end - dt.timedelta(days=7)
    resp = client.get(
        "/market/ohlcv/daily",
        params={"symbol": "AAPL", "start": start.isoformat(), "end": end.isoformat()},
    )
    assert resp.status_code == 200
    rows = resp.json()
    if not rows:
        pytest.skip("No OHLCV data returned; likely offline or provider unavailable")
    first = rows[0]
    for key in ("ts", "open", "high", "low", "close", "volume"):
        assert key in first

