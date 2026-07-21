from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import hashlib, uuid
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.photo import Photo
from app.schemas.photo import PhotoResponse
from app.storage import save_file
from app.exif_utils import extract_exif

router = APIRouter(prefix="/photos", tags=["photos"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/heic"}

@router.post("/upload", response_model=PhotoResponse, status_code=201)
async def upload_photo(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=422, detail="Unsupported file type")
    data = await file.read()
    sha256_hash = hashlib.sha256(data).hexdigest()    

    photo = (await db.execute(select(Photo).where(Photo.sha256_hash == sha256_hash, Photo.user_id == current_user.id))).scalar_one_or_none()
    if photo:
        raise HTTPException(status_code=409, detail="Duplicate photo")

    blob_path = f"{current_user.id}/{uuid.uuid4()}/{file.filename}"
    exif = extract_exif(data)
    save_file(blob_path, data)

    photo = Photo(
        user_id=current_user.id,
        original_filename=file.filename,
        blob_path=blob_path,
        file_size=file.size,
        mime_type=file.content_type,
        sha256_hash=sha256_hash,
        taken_at=exif["taken_at"],
        camera_make=exif["camera_make"],
        camera_model=exif["camera_model"],
        latitude=exif["latitude"],
        longitude=exif["longitude"]
        )
    
    db.add(photo)
    await db.commit()
    await db.refresh(photo)

    return photo


