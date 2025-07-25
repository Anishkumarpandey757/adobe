from fastapi import APIRouter, HTTPException
from app.db import get_db

router = APIRouter()

@router.get("/headings/{pdf_name}")
async def get_headings(pdf_name: str):
    """
    Fetch all heading spans for a given PDF from the spans collection.
    """
    db = get_db()
    cursor = db.spans.find({"pdf_name": pdf_name})
    spans = []
    async for doc in cursor:
        spans.append(doc)

    if not spans:
        raise HTTPException(status_code=404, detail="No spans found for this PDF.")

    # Heuristic: consider bold and large font as headings
    font_sizes = [s["font_size"] for s in spans if "font_size" in s]
    if not font_sizes:
        return []

    unique_sizes = sorted(set(font_sizes), reverse=True)
    h1_thresh = unique_sizes[0]
    h2_thresh = unique_sizes[1] if len(unique_sizes) > 1 else h1_thresh
    h3_thresh = unique_sizes[2] if len(unique_sizes) > 2 else h2_thresh

    headings = []
    for s in spans:
        if s.get("font_weight") == "bold" and s.get("font_size", 0) >= h3_thresh:
            # Assign level based on font size
            if s["font_size"] == h1_thresh:
                level = "H1"
            elif s["font_size"] == h2_thresh:
                level = "H2"
            else:
                level = "H3"
            headings.append({
                "text": s["text"],
                "level": level,
                "font_name": s["font_name"],
                "font_size": s["font_size"],
                "font_weight": s["font_weight"],
                "page": s["page"],
                "bbox": s["bbox"]
            })

    return headings 