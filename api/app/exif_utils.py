from PIL import Image, ExifTags
import io
from datetime import datetime, timezone


def extract_exif(data: bytes) -> dict:
    result = {
        "taken_at": None,
        "camera_make": None,
        "camera_model": None,
        "latitude": None,
        "longitude": None,
    }
    try:
        img = Image.open(io.BytesIO(data))
        raw = img._getexif()
        if not raw:
            return result

        exif = {ExifTags.TAGS.get(k, k): v for k, v in raw.items()}

        if "DateTimeOriginal" in exif:
            try:
                result["taken_at"] = datetime.strptime(
                    exif["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S"
                ).replace(tzinfo=timezone.utc)
            except ValueError:
                pass

        result["camera_make"] = exif.get("Make")
        result["camera_model"] = exif.get("Model")

        gps = exif.get("GPSInfo")
        if gps:
            gps_tags = {ExifTags.GPSTAGS.get(k, k): v for k, v in gps.items()}
            lat = _dms_to_decimal(gps_tags.get("GPSLatitude"), gps_tags.get("GPSLatitudeRef"))
            lon = _dms_to_decimal(gps_tags.get("GPSLongitude"), gps_tags.get("GPSLongitudeRef"))
            result["latitude"] = lat
            result["longitude"] = lon
    except Exception:
        pass

    return result


def _dms_to_decimal(dms, ref) -> float | None:
    if not dms or not ref:
        return None
    degrees, minutes, seconds = dms
    decimal = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
    if ref in ("S", "W"):
        decimal = -decimal
    return decimal
