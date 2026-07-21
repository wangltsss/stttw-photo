from azure.storage.blob.aio import BlobServiceClient
from app.config import settings

CONTAINER_NAME = "photos"


async def save_file(blob_path: str, data: bytes) -> None:
    async with BlobServiceClient.from_connection_string(settings.azure_storage_connection_string) as client:
        blob_client = client.get_blob_client(container=CONTAINER_NAME, blob=blob_path)
        await blob_client.upload_blob(data, overwrite=True)


async def download_file(blob_path: str) -> bytes:
    async with BlobServiceClient.from_connection_string(settings.azure_storage_connection_string) as client:
        blob_client = client.get_blob_client(container=CONTAINER_NAME, blob=blob_path)
        stream = await blob_client.download_blob()
        return await stream.readall()


async def delete_file(blob_path: str) -> None:
    async with BlobServiceClient.from_connection_string(settings.azure_storage_connection_string) as client:
        blob_client = client.get_blob_client(container=CONTAINER_NAME, blob=blob_path)
        await blob_client.delete_blob(delete_snapshots="include")
