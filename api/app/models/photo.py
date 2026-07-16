from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, ForeignKey
from app.database import Base
import uuid
from datetime import datetime, timezone


class Photo(Base):

    __tablename__ = "photos"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    original_filename: Mapped[str] = mapped_column(String(255))
    blob_path: Mapped[str] = mapped_column(String(512))
    file_size: Mapped[int] = mapped_column()
    mime_type: Mapped[str] = mapped_column(String(100))
    sha256_hash: Mapped[str] = mapped_column(String(64), index=True)
    taken_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    camera_make: Mapped[str | None] = mapped_column(String(100), nullable=True)
    camera_model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    latitude: Mapped[float | None] = mapped_column(nullable=True)
    longitude: Mapped[float | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
