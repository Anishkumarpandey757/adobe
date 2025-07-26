from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import os, tempfile, shutil, subprocess, sys
from pdf_pipeline.parse_pdf import parse_pdf
from pdf_pipeline.parse_docx import parse_docx
from pdf_pipeline.heading_detection import detect_headings
from pdf_pipeline.mongo_utils import insert_spans, insert_outline, insert_sections
from app.db import get_db
from dotenv import load_dotenv
from app.headings_api import router as headings_router
from pdf_pipeline.ingest import extract_sections

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(headings_router)

class OutlineResponse(BaseModel):
    pdf_name: str
    title: str
    outline: list

class SectionMeta(BaseModel):
    section_id: str
    level: str
    text: str
    page_start: int
    page_end: int

# Utility to list files in a directory
@app.get("/files/{folder}")
def list_files(folder: str):
    allowed = ["input", "output", "ground_truth", "uploaded_pdfs"]
    if folder not in allowed:
        raise HTTPException(status_code=400, detail="Invalid folder")
    dir_path = os.path.join(os.path.dirname(__file__), "..", folder)
    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    return {"files": files}

# Utility to download a file from a directory
@app.get("/files/{folder}/{filename}")
def download_file(folder: str, filename: str):
    allowed = ["input", "output", "ground_truth", "uploaded_pdfs"]
    if folder not in allowed:
        raise HTTPException(status_code=400, detail="Invalid folder")
    dir_path = os.path.join(os.path.dirname(__file__), "..", folder)
    file_path = os.path.join(dir_path, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=filename)

@app.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    # Save uploaded PDF to abode/uploaded_pdfs
    upload_dir = os.path.join(os.path.dirname(__file__), "..", "uploaded_pdfs")
    os.makedirs(upload_dir, exist_ok=True)
    upload_path = os.path.join(upload_dir, file.filename)
    with open(upload_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    # Automatically process the uploaded PDF and write output JSON
    output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(output_dir, exist_ok=True)
    # Call batch_extract.py as a module from the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    subprocess.run([
        sys.executable, "-m", "pdf_pipeline.batch_extract",
        "--input_dir", upload_dir,
        "--output_dir", output_dir
    ], check=True, cwd=project_root)
    # Now process the uploaded file for DB as before
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, file.filename)
        shutil.copyfile(upload_path, pdf_path)
        pdf_name = file.filename
        try:
            spans = parse_pdf(pdf_path)
        except Exception:
            spans = parse_docx(pdf_path)
        for span in spans:
            span['pdf_name'] = pdf_name
            await get_db().spans.insert_one(span)
        outline = detect_headings(spans, pdf_name)
        await get_db().outlines.insert_one({"pdf_name": pdf_name, **outline})
        # --- New: Extract and insert sections automatically ---
        sections = extract_sections(spans, outline)
        for section in sections:
            section['pdf_name'] = pdf_name
            await get_db().sections.insert_one(section)
        return {"outline_id": str(pdf_name)}

@app.get("/outline/{pdf_name}", response_model=OutlineResponse)
async def get_outline(pdf_name: str):
    doc = await get_db().outlines.find_one({"pdf_name": pdf_name})
    if not doc:
        raise HTTPException(status_code=404, detail="Outline not found")
    return OutlineResponse(pdf_name=doc['pdf_name'], title=doc['title'], outline=doc['outline'])

@app.get("/sections/{pdf_name}", response_model=list[SectionMeta])
async def get_sections(pdf_name: str):
    cursor = get_db().sections.find({"pdf_name": pdf_name})
    sections = []
    async for doc in cursor:
        sections.append(SectionMeta(
            section_id=doc['section_id'],
            level=doc['level'],
            text=doc['text'],
            page_start=doc['page_start'],
            page_end=doc['page_end']
        ))
    return sections 