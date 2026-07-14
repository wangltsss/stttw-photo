from fastapi import FastAPI
from app.config import settings
from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    environment: str

app = FastAPI(title="Photo API", version="0.1.0", docs_url="/docs")

@app.get("/health")
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", environment=settings.environment)

