import datetime as dt

from fastapi.testclient import TestClient

from apps.uyo_ai_api.app import app


def _base_body() -> dict:
    now = dt.datetime.now(dt.timezone.utc)
    start = now - dt.timedelta(days=1)
    return {
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


def test_invalid_side() -> None:
    client = TestClient(app)
    body = _base_body()
    body["fills"][0]["side"] = "BUYSELL"
    resp = client.post("/exec/kpis", params={"symbol": "AAPL"}, json=body)
    assert resp.status_code == 422


def test_non_positive_qty() -> None:
    client = TestClient(app)
    body = _base_body()
    body["fills"][0]["qty"] = 0
    resp = client.post("/exec/kpis", params={"symbol": "AAPL"}, json=body)
    assert resp.status_code == 422


def test_non_positive_price() -> None:
    client = TestClient(app)
    body = _base_body()
    body["fills"][0]["price"] = -1
    resp = client.post("/exec/kpis", params={"symbol": "AAPL"}, json=body)
    assert resp.status_code == 422
