import { useEffect, useState } from "react";
import { fetchPublicPhotos, thumbnailUrl, type Photo } from "../api";

export default function Gallery() {
  const [photos, setPhotos] = useState<Photo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {                             
    
    async function load() {
      try {
        const result = await fetchPublicPhotos();
        setPhotos(result);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    }

    load();

  }, []);

  if (loading) return <div className="page"><p className="loading">Loading...</p></div>;
  if (error) return <div className="page"><p className="error">{error}</p></div>;

  return (
    <div className="page">
      <nav>
        <h1>Photography</h1>
        <span>{photos.length} photos</span>
      </nav>

      {photos.length === 0 && <p className="empty">No photos yet.</p>}

      <div className="photo-grid">
        {photos.map((photo) => (
          <div key={photo.id} className="photo-card">
            <img src={thumbnailUrl(photo.id)} alt={photo.original_filename}/>
            <div className="photo-meta">
              <p>{photo.taken_at ? new Date(photo.taken_at).getFullYear() : "Unknown date" }</p>
              {photo.camera_make && `${photo.camera_make} ${photo.camera_model ?? ""}`}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
