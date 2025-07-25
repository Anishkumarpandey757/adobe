import React, { useEffect, useState } from "react";
import axios from "axios";

function nestOutline(outline) {
  const result = [];
  let currentH1 = null, currentH2 = null;
  outline.forEach(item => {
    if (item.level === "H1") {
      currentH1 = { ...item, children: [] };
      result.push(currentH1);
      currentH2 = null;
    } else if (item.level === "H2" && currentH1) {
      currentH2 = { ...item, children: [] };
      currentH1.children.push(currentH2);
    } else if (item.level === "H3" && currentH2) {
      currentH2.children.push(item);
    } else if (item.level === "H2") {
      result.push({ ...item, children: [] });
      currentH2 = result[result.length - 1];
    } else if (item.level === "H3") {
      result.push(item);
    }
  });
  return result;
}

function renderTree(nodes, level = 1) {
  return (
    <ul className={`ml-${level * 2}`}>
      {nodes.map((node, idx) => (
        <li key={idx} className={`py-1 font-semibold text-blue-${700 - level * 100}`}>
          <span>
            {node.level}: {node.text} <span className="text-xs text-gray-400">(p.{node.page})</span>
          </span>
          {node.children && node.children.length > 0 && renderTree(node.children, level + 1)}
        </li>
      ))}
    </ul>
  );
}

export default function OutlineViewer({ pdfName }) {
  const [outline, setOutline] = useState(null);

  useEffect(() => {
    if (!pdfName) return;
    axios.get(`http://localhost:8000/outline/${pdfName}`)
      .then(res => {
        setOutline(res.data);
        console.log("Fetched outline:", res.data); // Debug log
      })
      .catch(() => setOutline(null));
  }, [pdfName]);

  if (!outline) return <div className="text-gray-500">No outline loaded.</div>;

  if (!outline.outline || outline.outline.length === 0) {
    return <p className="text-red-500">No outline detected. Please ensure headings are extracted with levels (H1/H2/H3).</p>;
  }

  const onlyH1 = outline.outline.every(h => h.level === "H1");
  const nested = nestOutline(outline.outline);

  return (
    <div className="p-4 bg-white rounded shadow">
      <h2 className="text-xl font-bold mb-2">{outline.title}</h2>
      {onlyH1 && (
        <p className="text-yellow-600 text-sm mb-2">All headings are marked as H1. Please verify heading detection logic.</p>
      )}
      {renderTree(nested)}
    </div>
  );
} 