const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export interface Photo {
  id: string;
  original_filename: string;
  taken_at: string | null;
  camera_make: string | null;
  camera_model: string | null;
  thumbnail_path: string | null;
  created_at: string;
}

export async function fetchPublicPhotos(): Promise<Photo[]> {
  const res = await fetch(`${API_BASE}/photos/public`);
  if (!res.ok) throw new Error("Failed to fetch photos");
  return res.json();
}

export function thumbnailUrl(photoId: string): string {
  return `${API_BASE}/photos/${photoId}/thumbnail`;
}

export async function login(email: string, password: string): Promise<string> {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error("Invalid credentials");
  const data = await res.json();
  return data.access_token;
}

export async function uploadPhoto(token: string, file: File): Promise<void> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_BASE}/photos/upload`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });
  if (res.status === 409) throw new Error("Duplicate photo");
  if (!res.ok) throw new Error("Upload failed");
}
