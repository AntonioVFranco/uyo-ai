import datetime as dt

from fastapi.testclient import TestClient

from apps.uyo_ai_api.app import app


def test_exec_kpis_success() -> None:
    client = TestClient(app)
    now = dt.datetime.now(dt.timezone.utc)
    start = now - dt.timedelta(days=1)

    body = {
        "window": {"start": start.isoformat(), "end": now.isoformat()},
        "fills": [
            {
                "order_id": "t-1",
                "symbol": "AAPL",
                "ts": start.isoformat(),
                "side": "BUY",
                "qty": 1.0,
                "price": 100.0,
            }
        ],
    }

    resp = client.post("/exec/kpis", params={"symbol": "AAPL"}, json=body)
    assert resp.status_code == 200
    data = resp.json()
    for key in ("is_bps", "vwap_shortfall_bps", "twap_shortfall_bps"):
        assert key in data
