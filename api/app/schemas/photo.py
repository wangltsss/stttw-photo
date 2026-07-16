from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime


class PhotoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    original_filename: str
    blob_path: str
    file_size: int
    mime_type: str
    sha256_hash: str
    taken_at: datetime | None
    camera_make: str | None
    camera_model: str | None
    latitude: float | None
    longitude: float | None
    created_at: datetime
