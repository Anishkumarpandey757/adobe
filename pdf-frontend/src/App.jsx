import React, { useState } from "react";
import PdfUploadForm from "./components/PdfUploadForm";
import OutlineViewer from "./components/OutlineViewer";
import SummaryList from "./components/SummaryList";
import HeadingsList from "./components/HeadingsList";

function App() {
  const [pdfName, setPdfName] = useState("");
  const [showResults, setShowResults] = useState(false);

  const handleUpload = (outlineId) => {
    // outline_id is actually the PDF name from the backend
    setPdfName(outlineId);
    setShowResults(true);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <PdfUploadForm onUpload={handleUpload} />
      {showResults && pdfName && (
        <div className="w-full max-w-6xl mx-auto space-y-6 p-8">
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold mb-4 text-center">Analysis Results for: {pdfName}</h2>
          </div>
          <OutlineViewer pdfName={pdfName} />
          <HeadingsList pdfName={pdfName} />
          <SummaryList pdfName={pdfName} />
        </div>
      )}
    </div>
  );
}

export default App; 