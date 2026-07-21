import asyncio
import io
import logging
import uuid

from PIL import Image
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models.job import Job
from app.models.photo import Photo
from app.storage import download_file, save_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

THUMBNAIL_SIZE = (300, 300)
POLL_INTERVAL = 2


async def handle_thumbnail(payload: dict) -> None:
    photo_id = uuid.UUID(payload["photo_id"])
    blob_path = payload["blob_path"]

    # 1. download the original file bytes from Azure
    # 2. open with PIL: Image.open(io.BytesIO(data))
    # 3. resize: img.thumbnail(THUMBNAIL_SIZE)  — maintains aspect ratio
    # 4. write to a buffer: buf = io.BytesIO(); img.save(buf, format="JPEG"); buf.seek(0)
    # 5. thumbnail_path = f"thumbnails/{blob_path}"
    # 6. await save_file(thumbnail_path, buf.read())
    # 7. update the photo row:
    #      async with AsyncSessionLocal() as db:
    #          async with db.begin():
    #              result = await db.execute(select(Photo).where(Photo.id == photo_id))
    #              photo = result.scalar_one()
    #              photo.thumbnail_path = thumbnail_path
    ...


async def process_next_job() -> None:
    async with AsyncSessionLocal() as db:
        async with db.begin():
            result = await db.execute(
                select(Job)
                .where(Job.status == "pending")
                .order_by(Job.created_at)
                .limit(1)
                .with_for_update(skip_locked=True)
            )
            job = result.scalar_one_or_none()
            if not job:
                return
            job.status = "processing"

        logger.info(f"Processing job {job.id} type={job.type}")

        try:
            if job.type == "generate_thumbnail":
                await handle_thumbnail(job.payload)
            async with db.begin():
                job.status = "done"
        except Exception as e:
            logger.error(f"Job {job.id} failed: {e}")
            async with db.begin():
                job.status = "failed"
                job.error = str(e)[:500]


async def main() -> None:
    logger.info("Worker started, polling every %ds", POLL_INTERVAL)
    while True:
        try:
            await process_next_job()
        except Exception as e:
            logger.error(f"Unexpected worker error: {e}")
        await asyncio.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
