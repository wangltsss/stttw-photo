from fastapi import FastAPI
from app.config import settings
from pydantic import BaseModel
from app.routers import auth

class HealthResponse(BaseModel):
    status: str
    environment: str

app = FastAPI(title="Photo API", version="0.1.0", docs_url="/docs")
app.include_router(auth.router)

@app.get("/health")
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", environment=settings.environment)

