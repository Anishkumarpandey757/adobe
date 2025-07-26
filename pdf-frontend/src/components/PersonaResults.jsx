import React, { useState, useEffect } from "react";
import axios from "axios";

export default function PersonaResults() {
  const [persona, setPersona] = useState("");
  const [job, setJob] = useState("");
  const [pdfs, setPdfs] = useState([]);
  const [selectedPdfs, setSelectedPdfs] = useState([]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [processingStatus, setProcessingStatus] = useState("");

  useEffect(() => {
    axios.get("http://localhost:8000/files/uploaded_pdfs")
      .then(res => setPdfs(res.data.files || []));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResults(null);
    setProcessingStatus("Initializing models...");
    
    try {
      setProcessingStatus("Encoding persona and job...");
      const response = await axios.post("http://localhost:8000/persona-query", {
        persona,
        job,
        pdf_names: selectedPdfs,
        top_k: 5
      });
      setResults(response.data);
      setProcessingStatus("Analysis complete!");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to fetch results. Please check your backend and input.");
      setProcessingStatus("");
    }
    setLoading(false);
  };

  const handleSelectAll = () => {
    if (selectedPdfs.length === pdfs.length) {
      setSelectedPdfs([]);
    } else {
      setSelectedPdfs(pdfs);
    }
  };

  return (
    <div className="p-6 bg-white rounded shadow mt-4">
      <h2 className="text-xl font-bold mb-4">Persona-Driven Document Intelligence (Round 1B)</h2>
      <p className="text-gray-600 mb-6">Analyze 8-10 PDFs using AI-powered persona-driven insights</p>
      
      <form onSubmit={handleSubmit} className="mb-6 space-y-4">
        <div>
          <label className="block font-semibold mb-1">Persona</label>
          <input 
            type="text" 
            className="w-full border rounded px-2 py-1" 
            value={persona} 
            onChange={e => setPersona(e.target.value)} 
            placeholder="e.g., PhD Researcher in Computational Biology"
            required 
          />
        </div>
        <div>
          <label className="block font-semibold mb-1">Job to be Done</label>
          <input 
            type="text" 
            className="w-full border rounded px-2 py-1" 
            value={job} 
            onChange={e => setJob(e.target.value)} 
            placeholder="e.g., Prepare a comprehensive literature review focusing on methodologies"
            required 
          />
        </div>
        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="block font-semibold">Select PDFs (3-10 required for Round 1B)</label>
            <button 
              type="button" 
              onClick={handleSelectAll}
              className="text-sm text-blue-600 hover:text-blue-800"
            >
              {selectedPdfs.length === pdfs.length ? "Deselect All" : "Select All"}
            </button>
          </div>
          <div className="max-h-40 overflow-y-auto border rounded p-2">
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {pdfs.map(pdf => (
                <label key={pdf} className="flex items-center space-x-2 text-sm">
                  <input
                    type="checkbox"
                    value={pdf}
                    checked={selectedPdfs.includes(pdf)}
                    onChange={e => {
                      if (e.target.checked) setSelectedPdfs([...selectedPdfs, pdf]);
                      else setSelectedPdfs(selectedPdfs.filter(f => f !== pdf));
                    }}
                  />
                  <span className="truncate">{pdf}</span>
                </label>
              ))}
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-1">
            Selected: {selectedPdfs.length} PDFs {selectedPdfs.length < 3 && "(Minimum 3 required)"}
          </p>
        </div>
        <button 
          type="submit" 
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400" 
          disabled={loading || selectedPdfs.length < 3 || selectedPdfs.length > 10}
        >
          {loading ? "Processing..." : "Analyze Documents"}
        </button>
      </form>
      
      {processingStatus && (
        <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded">
          <p className="text-blue-800">{processingStatus}</p>
        </div>
      )}
      
      {error && <div className="text-red-600 mb-4 p-3 bg-red-50 border border-red-200 rounded">{error}</div>}
      
      {results && (
        <div>
          <div className="mb-4 p-4 bg-gray-50 rounded">
            <h3 className="text-lg font-bold mb-2">Round 1B Analysis Summary</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="font-semibold">PDFs Processed:</span> {results.metadata.total_pdfs_processed}
              </div>
              <div>
                <span className="font-semibold">Persona:</span> {results.metadata.persona}
              </div>
              <div>
                <span className="font-semibold">Job:</span> {results.metadata.job_to_be_done}
              </div>
              <div>
                <span className="font-semibold">Processing Time:</span> {results.metadata.processing_time_seconds}s
              </div>
            </div>
            <div className="mt-2 text-xs text-gray-600">
              <span className="font-semibold">Models Used:</span> {results.metadata.models_used.embeddings}, {results.metadata.models_used.similarity}, {results.metadata.models_used.summarization}
            </div>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-bold mb-4">Extracted Sections</h3>
              <div className="space-y-3">
                {results.extracted_sections.map((section, idx) => (
                  <div key={idx} className="bg-white p-3 rounded border">
                    <div className="font-semibold text-blue-800">{section.document}</div>
                    <div className="text-sm text-gray-600">Page: {section.page_number} | Rank: {section.importance_rank}</div>
                    <div className="mt-1 text-gray-800">{section.section_title}</div>
                  </div>
                ))}
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-bold mb-4">Sub-section Analysis</h3>
              <div className="space-y-3">
                {results.sub_section_analysis.map((analysis, idx) => (
                  <div key={idx} className="bg-white p-3 rounded border">
                    <div className="font-semibold text-green-800">{analysis.document}</div>
                    <div className="text-sm text-gray-600">
                      Pages: {analysis.page_number_constraints.start}-{analysis.page_number_constraints.end}
                    </div>
                    <div className="mt-2 text-gray-800">
                      <span className="font-semibold">Refined Text:</span> {analysis.refined_text}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 