import React, { useRef, useState } from "react";
import axios from "axios";
import PersonaResults from "./PersonaResults";

export default function PdfUploadForm({ onUpload }) {
  const singleFileInput = useRef();
  const multipleFileInput = useRef();
  const [loading, setLoading] = useState(false);
  const [currentView, setCurrentView] = useState("round1a"); // "round1a", "round1b-upload", "round1b-analysis"
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [uploadedPdfs, setUploadedPdfs] = useState([]);

  const handleSingleUpload = async (e) => {
    e.preventDefault();
    const file = singleFileInput.current?.files?.[0];
    if (!file) return;
    
    setLoading(true);
    setError("");
    setSuccess("");
    
    const formData = new FormData();
    formData.append("file", file);
    
    try {
      const res = await axios.post("http://localhost:8000/ingest/pdf", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      onUpload(res.data.outline_id);
      setUploadedPdfs(prev => [...prev, file.name]);
      setSuccess(`✅ Successfully uploaded and processed "${file.name}". Results are displayed below.`);
      singleFileInput.current.value = "";
    } catch (err) {
      if (err.message === "Network Error") {
        setError("Backend server is not running. Please start the backend server first.");
      } else {
        setError("Upload failed: " + (err.response?.data?.detail || err.message));
      }
    } finally {
      setLoading(false);
    }
  };

  const handleMultipleUpload = async (e) => {
    e.preventDefault();
    const files = multipleFileInput.current?.files;
    if (!files || files.length === 0) return;
    
    const fileArray = Array.from(files);
    if (fileArray.length < 3) {
      setError("Please select at least 3 PDFs for Round 1B analysis.");
      return;
    }
    if (fileArray.length > 10) {
      setError("Please select maximum 10 PDFs for Round 1B analysis.");
      return;
    }
    
    setLoading(true);
    setError("");
    setSuccess("");
    
    try {
      const uploadedNames = [];
      for (const file of fileArray) {
        const formData = new FormData();
        formData.append("file", file);
        await axios.post("http://localhost:8000/ingest/pdf", formData, {
          headers: { "Content-Type": "multipart/form-data" }
        });
        uploadedNames.push(file.name);
      }
      setUploadedPdfs(prev => [...prev, ...uploadedNames]);
      setSuccess(`✅ Successfully uploaded ${uploadedNames.length} PDFs for Round 1B analysis.`);
      setCurrentView("round1b-analysis");
      multipleFileInput.current.value = "";
    } catch (err) {
      if (err.message === "Network Error") {
        setError("Backend server is not running. Please start the backend server first.");
      } else {
        setError("Upload failed: " + (err.response?.data?.detail || err.message));
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full">
      {/* Navigation Bar */}
      <nav className="bg-white shadow-lg mb-6">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <span className="text-xl font-bold text-gray-800">
                Abode PDF Intelligence
              </span>
            </div>
            <div className="flex items-center space-x-8">
              <button 
                onClick={() => setCurrentView("round1a")}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  currentView === "round1a"
                    ? "bg-blue-500 text-white" 
                    : "text-gray-600 hover:text-gray-900"
                }`}
              >
                Round 1A: PDF Upload & Analysis
              </button>
              <button 
                onClick={() => setCurrentView("round1b-upload")}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  currentView === "round1b-upload"
                    ? "bg-green-500 text-white" 
                    : "text-gray-600 hover:text-gray-900"
                }`}
              >
                Round 1B: Upload PDFs
              </button>
              <button 
                onClick={() => setCurrentView("round1b-analysis")}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  currentView === "round1b-analysis"
                    ? "bg-purple-500 text-white" 
                    : "text-gray-600 hover:text-gray-900"
                }`}
              >
                Round 1B: Persona Analysis
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="min-h-screen bg-gray-100 flex flex-col items-center p-8">
        {currentView === "round1a" && (
          // Round 1A: Single PDF Upload
          <div className="w-full max-w-4xl">
            <h1 className="text-2xl font-bold mb-6 text-center">Round 1A: PDF Outline & Summary Viewer</h1>
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <form onSubmit={handleSingleUpload} className="flex items-center gap-2 mb-4">
                <input type="file" accept="application/pdf" ref={singleFileInput} className="border p-2 rounded flex-1" />
                <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700" disabled={loading}>
                  {loading ? "Uploading..." : "Upload PDF"}
                </button>
              </form>
              {error && (
                <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded text-red-600">
                  {error}
                </div>
              )}
              {success && (
                <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded text-green-600">
                  {success}
                </div>
              )}
              <p className="text-sm text-gray-600">
                Upload a PDF to extract headings, outlines, and summaries. This is Round 1A functionality.
              </p>
              {uploadedPdfs.length > 0 && (
                <div className="mt-4">
                  <h4 className="font-semibold text-sm text-gray-700">Uploaded PDFs:</h4>
                  <ul className="text-sm text-gray-600">
                    {uploadedPdfs.map((pdf, idx) => (
                      <li key={idx}>• {pdf}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}

        {currentView === "round1b-upload" && (
          // Round 1B: Multiple PDF Upload
          <div className="w-full max-w-4xl">
            <h1 className="text-2xl font-bold mb-6 text-center">Round 1B: Upload PDFs for Persona Analysis</h1>
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <form onSubmit={handleMultipleUpload} className="mb-4">
                <div className="mb-4">
                  <label className="block font-semibold mb-2">Select 3-10 PDFs for Analysis</label>
                  <input 
                    type="file" 
                    accept="application/pdf" 
                    multiple 
                    ref={multipleFileInput} 
                    className="border p-2 rounded w-full" 
                  />
                </div>
                <button type="submit" className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700" disabled={loading}>
                  {loading ? "Uploading..." : "Upload PDFs for Round 1B Analysis"}
                </button>
              </form>
              {error && (
                <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded text-red-600">
                  {error}
                </div>
              )}
              {success && (
                <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded text-green-600">
                  {success}
                </div>
              )}
              <p className="text-sm text-gray-600">
                Upload 3-10 PDFs that you want to analyze with persona-driven intelligence. After upload, go to "Round 1B: Persona Analysis" to start the analysis.
              </p>
            </div>
          </div>
        )}

        {currentView === "round1b-analysis" && (
          // Round 1B: Persona Analysis
          <div className="w-full max-w-6xl">
            <PersonaResults />
          </div>
        )}
      </div>
    </div>
  );
} 