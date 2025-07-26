from fastapi import APIRouter, HTTPException, Body
from app.db import get_db
from pdf_pipeline.persona_encoder import encode_persona_job
from pdf_pipeline.relevance import encode_sections, score_sections
from pdf_pipeline.summarize import summarize_section
import os
from datetime import datetime
import time

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

@router.get("/summaries/{pdf_name}/{section_id}")
async def get_summary(pdf_name: str, section_id: str):
    """
    Fetch summary for a specific section of a PDF.
    """
    db = get_db()
    try:
        section_id_int = int(section_id)
        summary_doc = await db.summaries.find_one({
            "pdf_name": pdf_name,
            "section_id": section_id_int
        })
        
        if not summary_doc:
            raise HTTPException(status_code=404, detail="Summary not found")
        
        return {"summary_text": summary_doc.get("summary", "No summary available")}
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid section ID")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching summary: {str(e)}")

@router.post("/persona-query")
async def persona_query(
    persona: str = Body(...),
    job: str = Body(...),
    pdf_names: list = Body(...),
    top_k: int = Body(5)
):
    """
    Round 1B: Persona-Driven Document Intelligence
    Given persona, job, and a list of pdf_names (3-10 PDFs), return top relevant sections per document.
    Uses MiniLM embeddings, cosine similarity, and TextRank summarization.
    CPU-only, ≤1GB model size, ≤60 seconds processing time.
    """
    start_time = time.time()
    
    # Validate input according to Round 1B requirements
    if len(pdf_names) < 3:
        raise HTTPException(status_code=400, detail="Minimum 3 PDFs required for Round 1B")
    if len(pdf_names) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 PDFs allowed for Round 1B")
    if not persona.strip() or not job.strip():
        raise HTTPException(status_code=400, detail="Persona and job descriptions cannot be empty")
    
    db = get_db()
    persona_job = f"{persona}. {job}"
    
    try:
        # Step 1: Encode persona/job using MiniLM-L6-v2 (CPU-only)
        persona_emb = encode_persona_job(persona_job)
        
        extracted_sections = []
        sub_section_analysis = []
        processed_count = 0
        
        for pdf_name in pdf_names:
            try:
                # Step 2: Fetch sections from MongoDB
                cursor = db.sections.find({"pdf_name": pdf_name})
                sections = []
                section_texts = []
                section_metas = []
                
                async for doc in cursor:
                    if doc.get("text") and len(doc["text"].strip()) > 10:  # Filter out very short sections
                        section_texts.append(doc["text"])
                        section_metas.append(doc)
                
                if not section_texts:
                    continue
                
                # Step 3: Encode sections using MiniLM-L6-v2
                section_embs = encode_sections(section_texts)
                
                # Step 4: Score sections using cosine similarity
                scores = score_sections(persona_emb, section_embs)
                
                # Step 5: Rank and get top sections
                ranked = sorted(zip(section_metas, scores), key=lambda x: -x[1])
                
                for rank, (meta, score) in enumerate(ranked[:top_k], 1):
                    try:
                        # Step 6: Summarize using TextRank (sumy)
                        refined_text = summarize_section(meta["text"], sentences_count=2)
                        
                        # Extract section title (first 100 chars)
                        section_title = meta.get("text", "")[:100]
                        if len(section_title) == 100:
                            section_title += "..."
                        
                        # 1. Extracted Section (Round 1B format)
                        extracted_sections.append({
                            "document": pdf_name,
                            "page_number": meta.get("page_start", 0),
                            "section_title": section_title,
                            "importance_rank": rank
                        })
                        
                        # 2. Sub-section Analysis (Round 1B format)
                        sub_section_analysis.append({
                            "document": pdf_name,
                            "refined_text": refined_text,
                            "page_number_constraints": {
                                "start": meta.get("page_start", 0),
                                "end": meta.get("page_end", meta.get("page_start", 0))
                            }
                        })
                        
                    except Exception as e:
                        # If summarization fails, use first few sentences
                        text = meta["text"]
                        sentences = text.split('.')[:2]
                        refined_text = '. '.join(sentences) + '.'
                        
                        # Extract section title (first 100 chars)
                        section_title = meta.get("text", "")[:100]
                        if len(section_title) == 100:
                            section_title += "..."
                        
                        extracted_sections.append({
                            "document": pdf_name,
                            "page_number": meta.get("page_start", 0),
                            "section_title": section_title,
                            "importance_rank": rank
                        })
                        
                        sub_section_analysis.append({
                            "document": pdf_name,
                            "refined_text": refined_text,
                            "page_number_constraints": {
                                "start": meta.get("page_start", 0),
                                "end": meta.get("page_end", meta.get("page_start", 0))
                            }
                        })
                
                processed_count += 1
                
            except Exception as e:
                # Log error but continue with other PDFs
                print(f"Error processing {pdf_name}: {str(e)}")
                continue
        
        processing_time = time.time() - start_time
        
        if not extracted_sections:
            raise HTTPException(status_code=404, detail="No valid sections found in any of the selected PDFs")
        
        # Round 1B Output Format
        return {
            "metadata": {
                "input_documents": pdf_names,
                "persona": persona,
                "job_to_be_done": job,
                "processing_timestamp": datetime.utcnow().isoformat() + "Z",
                "processing_time_seconds": round(processing_time, 2),
                "total_pdfs_processed": processed_count,
                "models_used": {
                    "embeddings": "MiniLM-L6-v2",
                    "similarity": "cosine_similarity",
                    "summarization": "TextRank (sumy)"
                }
            },
            "extracted_sections": extracted_sections,
            "sub_section_analysis": sub_section_analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}") 