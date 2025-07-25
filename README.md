# Intelligent PDF Heading Extraction Pipeline

## Overview
This project provides an offline, CPU-only, Dockerized pipeline for extracting document outlines/headings from PDFs. It supports English, Spanish, Japanese, and other languages using a combination of font heuristics and a DistilBERT-based classifier. The solution is designed for batch processing and evaluation, with all dependencies included in the Docker image.

---

## Approach
- **PDFs are parsed** using PyMuPDF (fitz) for direct extraction; fallback to DOCX via LibreOffice and python-docx if needed.
- **Text spans** are extracted with font, size, weight, and position info.
- **Heading detection** uses font size thresholds, boldness, regex, and a DistilBERT classifier (≤200MB, loaded at build time, CPU-only).
- **Batch processing**: All PDFs in `/app/input` are processed, and a JSON outline is written to `/app/output` for each.
- **Multilingual**: The pipeline works for English, Spanish, Japanese, and more (see evaluation results).
- **Evaluation**: Precision, recall, and F1 are computed against ground truth JSONs.

---

## Models and Libraries Used
- **PyMuPDF (fitz)**: PDF parsing
- **python-docx**: DOCX parsing (fallback)
- **transformers, torch**: DistilBERT classifier for heading detection
- **numpy, scikit-learn**: Heuristics and thresholds
- **LibreOffice**: PDF to DOCX conversion
- **FastAPI**: API for upload/testing (optional)
- **All dependencies are installed in the Docker image**

---

## Dockerfile
- Uses `python:3.10-slim` (AMD64, CPU-only)
- Installs all dependencies and downloads the model at build time
- Entry point: batch extraction script for `/app/input` → `/app/output`

---

## How to Build and Run (Batch Extraction)

### 1. Build the Docker Image
```bash
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .
```

### 2. Prepare Input and Output Folders
- Place your PDFs in `abode/input` (or whichever folder you want to mount as `/app/input`).
- Ensure `abode/output` exists for results.

### 3. Run the Docker Container
```bash
docker run --rm -v %cd%/abode/input:/app/input -v %cd%/abode/output:/app/output --network none mysolutionname:somerandomidentifier
```
- On Linux/macOS, use `$(pwd)` instead of `%cd%`.

### 4. Check the Output
- Output JSONs will be in `abode/output` on your host machine.

### 5. Evaluate (Optional, outside Docker)
```bash
python evaluate.py --pred_dir abode/output --gt_dir abode/ground_truth
```

---

## Output Format Example
For each PDF, the output JSON will look like:
```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 1 },
    ...
  ]
}
```

---

## Sample Evaluation Results
The pipeline supports multilingual heading extraction (English, Spanish, Japanese, etc.).

Example evaluation output:
```
english_sample_4.json: Precision=1.00, Recall=1.00
english_sample_5.json: Precision=1.00, Recall=1.00
multilang_sample_2.json: Precision=1.00, Recall=1.00
multilang_sample_5.json: Precision=1.00, Recall=1.00
sample_test_headings.json: Precision=0.86, Recall=1.00

Overall: Precision=0.96, Recall=1.00, F1=0.98
```
- **English, Spanish, and Japanese PDFs** are supported and evaluated.
- Metrics are computed using `evaluate.py` as described above.

---

## Troubleshooting
- If you get a permissions error, make sure your input/output folders exist and are accessible.
- If you get a model download error, ensure the model is downloaded at build time (as in your Dockerfile).
- If you need to process PDFs from `uploaded_pdfs`, mount that folder as `/app/input`.

---

## Summary Table
| Step                | Command/Action                                                                 |
|---------------------|-------------------------------------------------------------------------------|
| Build image         | `docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .` |
| Run container       | `docker run --rm -v %cd%/abode/input:/app/input -v %cd%/abode/output:/app/output --network none mysolutionname:somerandomidentifier` |
| Check output        | See `abode/output`                                                            |
| Evaluate            | `python evaluate.py --pred_dir abode/output --gt_dir abode/ground_truth`       |

---

## File Structure
```
abode/
├─ input/           # Place PDFs here for batch processing
├─ output/          # Batch extraction JSONs will appear here
├─ ground_truth/    # Place ground truth JSONs here for evaluation
├─ uploaded_pdfs/   # PDFs uploaded via API are saved here
├─ app/
│   ├─ main.py      # FastAPI backend
│   ├─ headings_api.py
│   ├─ db.py
├─ pdf_pipeline/
│   ├─ batch_extract.py
│   ├─ parse_pdf.py
│   ├─ parse_docx.py
│   ├─ heading_detection.py
├─ evaluate.py      # Accuracy evaluation script
├─ requirements.txt
├─ Dockerfile
```

---

## Features Implemented

- **PDF Parsing**: Extracts text, font, and layout information from PDFs using PyMuPDF (fitz). Fallback to DOCX parsing via LibreOffice and python-docx for robust extraction.
- **MongoDB Integration**: Stores all extracted spans, outlines, and section metadata in MongoDB for further querying and analytics.
- **API Endpoints**: FastAPI backend provides endpoints for PDF upload, outline retrieval, section listing, file management, and evaluation.
- **Frontend**: React + Tailwind CSS frontend for uploading PDFs, visualizing outlines, headings, and summaries.
- **Batch Processing**: Dockerized batch pipeline processes all PDFs in a folder and outputs JSON outlines for each.
- **Evaluation**: Includes a script to compute precision, recall, and F1 against ground truth for heading detection.
- **Multilingual Support**: Handles English, Spanish, Japanese, and other languages using font heuristics and a DistilBERT classifier.
- **Offline, CPU-only, Dockerized**: All dependencies and models are included in the Docker image; no internet required at runtime.

---

## Credits
- PyMuPDF, python-docx, FastAPI, Motor, React, Tailwind CSS, Docker, transformers, torch, scikit-learn, numpy 