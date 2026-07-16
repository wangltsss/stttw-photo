from pathlib import Path

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


def save_file(blob_path: str, data: bytes) -> None:
    full_path = UPLOAD_DIR / blob_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_bytes(data)


def delete_file(blob_path: str) -> None:
    full_path = UPLOAD_DIR / blob_path
    if full_path.exists():
        full_path.unlink()
