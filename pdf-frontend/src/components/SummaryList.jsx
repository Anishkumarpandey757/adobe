import React, { useEffect, useState } from "react";
import axios from "axios";

export default function SummaryList({ pdfName }) {
  const [sections, setSections] = useState([]);
  const [selected, setSelected] = useState(null);
  const [summary, setSummary] = useState("");

  useEffect(() => {
    if (!pdfName) return;
    axios.get(`http://localhost:8000/sections/${pdfName}`)
      .then(res => setSections(res.data));
  }, [pdfName]);

  const fetchSummary = (sectionId) => {
    axios.get(`http://localhost:8000/summaries/${pdfName}/${sectionId}`)
      .then(res => setSummary(res.data.summary_text));
    setSelected(sectionId);
  };

  return (
    <div className="p-4 bg-white rounded shadow mt-4">
      <h2 className="text-lg font-bold mb-2">Sections</h2>
      <ul>
        {sections.map(sec => (
          <li key={sec.section_id}>
            <button
              className={`block w-full text-left py-1 px-2 rounded hover:bg-blue-100 ${selected === sec.section_id ? "bg-blue-200" : ""}`}
              onClick={() => fetchSummary(sec.section_id)}
            >
              {sec.level}: {sec.text} (p.{sec.page_start}-{sec.page_end})
            </button>
          </li>
        ))}
      </ul>
      {summary && (
        <div className="mt-4 p-2 bg-gray-50 border rounded">
          <h3 className="font-semibold">Summary</h3>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
} 