import React, { useState } from "react";
import PdfUploadForm from "./components/PdfUploadForm";
import OutlineViewer from "./components/OutlineViewer";
import SummaryList from "./components/SummaryList";
import HeadingsList from "./components/HeadingsList";

function App() {
  const [pdfName, setPdfName] = useState("");

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-8">
      <h1 className="text-2xl font-bold mb-6">PDF Outline & Summary Viewer</h1>
      <PdfUploadForm onUpload={setPdfName} />
      {pdfName && (
        <>
          <OutlineViewer pdfName={pdfName} />
          <HeadingsList pdfName={pdfName} />
          <SummaryList pdfName={pdfName} />
        </>
      )}
    </div>
  );
}

export default App; 