import { useState } from "react";
import { login, uploadPhoto } from "../api";

export default function Admin() {
  const [token, setToken] = useState<string | null>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState<string | null>(null);

  const [uploading, setUploading] = useState(false);
  const [uploadMsg, setUploadMsg] = useState<string | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoginError(null);
    try{
      const result = await login(email, password);
      setToken(result);
    } catch (err) {
      setLoginError((err as Error).message);
    }
  }

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file || !token) return;
    setUploading(true);
    setUploadMsg(null);
    setUploadError(null);
    try {
      await uploadPhoto(token, file);
      setUploadMsg("Uploaded: " + file.name)
      setUploading(false);
    } catch (err) {
      setUploadError((err as Error).message);
      setUploading(false);
    }
  }

  if (!token) {
    return (
      <div className="page">
        <div className="admin-form">
          <h2>Admin</h2>
          <form onSubmit={handleLogin}>
            <div className="field">
              <label>Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="field">
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit">Sign in</button>
            {loginError && <p className="error">{loginError}</p>}
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <nav>
        <h1>Admin</h1>
        <span onClick={() => setToken(null)} style={{ cursor: "pointer" }}>Sign out</span>
      </nav>

      <div className="upload-section">
        <div className="admin-form">
          <h2>Upload photo</h2>
          <input
            type="file"
            accept="image/jpeg,image/png,image/webp"
            onChange={handleUpload}
            disabled={uploading}
          />
          {uploading && <p className="loading">Uploading...</p>}
          {uploadMsg && <p className="success">{uploadMsg}</p>}
          {uploadError && <p className="error">{uploadError}</p>}
        </div>
      </div>
    </div>
  );
}
