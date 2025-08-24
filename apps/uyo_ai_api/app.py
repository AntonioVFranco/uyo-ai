
import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import datetime as dt

app = FastAPI(title="UYO AI API", version="0.1.0")

# CORS: allow local Streamlit UI origins only
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=600,
)


@app.middleware("http")
async def add_security_headers(request, call_next):
    """Attach basic security headers to all responses without breaking behavior.

    HSTS is opt-in via ENABLE_HSTS=1 to avoid local HTTP development issues.
    """

    response = await call_next(request)

    # Set headers only if they are not already present
    if "X-Content-Type-Options" not in response.headers:
        response.headers["X-Content-Type-Options"] = "nosniff"
    if "X-Frame-Options" not in response.headers:
        response.headers["X-Frame-Options"] = "DENY"
    if "Referrer-Policy" not in response.headers:
        response.headers["Referrer-Policy"] = "no-referrer"
    if "Permissions-Policy" not in response.headers:
        response.headers["Permissions-Policy"] = "interest-cohort=()"
    if "Cross-Origin-Opener-Policy" not in response.headers:
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    if "Cross-Origin-Resource-Policy" not in response.headers:
        response.headers["Cross-Origin-Resource-Policy"] = "same-site"
    if "Cache-Control" not in response.headers:
        response.headers["Cache-Control"] = "no-store"

    if os.getenv("ENABLE_HSTS", "0") == "1":
        response.headers.setdefault(
            "Strict-Transport-Security", "max-age=31536000; includeSubDomains"
        )

    return response


@app.get("/")
def index():
    """Redirect the API root to the interactive documentation."""
    return RedirectResponse(url="/docs")


class Fill(BaseModel):
    order_id: str
    symbol: str
    ts: dt.datetime
    side: Literal["BUY", "SELL"]
    qty: float = Field(gt=0)
    price: float = Field(gt=0)
    strategy: Optional[str] = None
    notes: Optional[str] = None


class Window(BaseModel):
    start: dt.datetime
    end: dt.datetime


class ExecKpiResponse(BaseModel):
    is_bps: float
    vwap_shortfall_bps: float
    twap_shortfall_bps: float


@app.get("/health")
def health():
    """Liveness probe endpoint for health checks."""
    return {"status": "ok"}


@app.post("/exec/kpis", response_model=ExecKpiResponse)
def exec_kpis(symbol: str, window: Window, fills: List[Fill]):
    """Compute execution KPIs for a symbol over a given window.

    This is a deterministic stub that returns fixed values to enable UI integration.
    """
    # Minimal stub for now; engines/execution will replace this logic
    # Return deterministic dummy values so the UI can integrate immediately.
    return ExecKpiResponse(is_bps=12.3, vwap_shortfall_bps=9.1, twap_shortfall_bps=11.0)
