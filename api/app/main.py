from fastapi import FastAPI
from app.config import settings
from pydantic import BaseModel
from app.routers import auth, photos
from fastapi.middleware.cors import CORSMiddleware



class HealthResponse(BaseModel):
    status: str
    environment: str

app = FastAPI(title="Photo API", version="0.1.0", docs_url="/docs")
app.include_router(auth.router)
app.include_router(photos.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", environment=settings.environment)

