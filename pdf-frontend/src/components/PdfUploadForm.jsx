import React, { useRef, useState } from "react";
import axios from "axios";

export default function PdfUploadForm({ onUpload }) {
  const fileInput = useRef();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!fileInput.current.files[0]) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", fileInput.current.files[0]);
    try {
      const res = await axios.post("http://localhost:8000/ingest/pdf", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      onUpload(res.data.outline_id);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-2 mb-4">
      <input type="file" accept="application/pdf" ref={fileInput} className="border p-2 rounded" />
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>
        {loading ? "Uploading..." : "Upload PDF"}
      </button>
    </form>
  );
} 