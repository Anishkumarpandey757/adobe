import React, { useEffect, useState } from "react";
import axios from "axios";

export default function HeadingsList({ pdfName }) {
  const [headings, setHeadings] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!pdfName) return;
    axios.get(`http://localhost:8000/headings/${pdfName}`)
      .then(res => {
        setHeadings(res.data);
        setError("");
      })
      .catch(err => {
        setHeadings([]);
        setError("No headings found or error fetching headings.");
      });
  }, [pdfName]);

  if (error) return <div className="text-red-500">{error}</div>;
  if (!headings.length) return <div className="text-gray-500">No headings to display.</div>;

  return (
    <div className="p-4 bg-white rounded shadow mt-4">
      <h2 className="text-lg font-bold mb-2">Detected Headings</h2>
      <ul>
        {headings.map((h, idx) => (
          <li key={idx} className="mb-2">
            <span className="font-semibold">{h.level}:</span> {h.text}
            <span className="ml-2 text-xs text-gray-500">
              (Font: {h.font_name}, Size: {h.font_size}, Page: {h.page})
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
} 