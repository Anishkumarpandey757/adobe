# Abode: Intelligent PDF Analysis Platform

## Overview
Abode is a comprehensive document intelligence platform that provides both **Round 1A: PDF Heading Extraction** and **Round 1B: Persona-Driven Document Intelligence**. The system is designed for offline, CPU-only operation with Docker deployment, supporting multilingual document processing and AI-powered content analysis.

---

## Round 1A: PDF Heading Extraction Pipeline

### Features
- **Multilingual Support**: English, Spanish, Japanese, and other languages
- **Robust PDF Parsing**: PyMuPDF (fitz) with DOCX fallback via LibreOffice
- **Intelligent Heading Detection**: Font heuristics + DistilBERT classifier (≤200MB)
- **Batch Processing**: Process multiple PDFs with structured JSON output
- **API & Frontend**: FastAPI backend with React frontend for interactive use

### Technical Stack
- **PDF Processing**: PyMuPDF (fitz), python-docx, LibreOffice
- **ML Models**: DistilBERT classifier, transformers, torch
- **Backend**: FastAPI, Motor (MongoDB), uvicorn
- **Frontend**: React, Tailwind CSS, Axios
- **Infrastructure**: Docker, MongoDB

---

## Round 1B: Persona-Driven Document Intelligence

### Theme: "Connect What Matters — For the User Who Matters"

**Challenge**: Build an intelligent document analyst that extracts and prioritizes the most relevant sections from 3-10 PDFs based on specific personas and their job-to-be-done requirements.

### Key Requirements
- **Input**: 3-10 related PDFs + Persona definition + Job-to-be-done
- **Output**: JSON format with metadata, extracted sections, and sub-section analysis
- **Constraints**: CPU-only, ≤1GB model size, ≤60 seconds processing time, offline operation
- **Generalization**: Must work across diverse domains and document types

### Sample Test Cases

#### Test Case 1: Academic Research
- **Documents**: 4 research papers on "Graph Neural Networks for Drug Discovery"
- **Persona**: PhD Researcher in Computational Biology
- **Job**: "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"

#### Test Case 2: Business Analysis
- **Documents**: 3 annual reports from competing tech companies (2022-2024)
- **Persona**: Investment Analyst
- **Job**: "Analyze revenue trends, R&D investments, and market positioning strategies"

#### Test Case 3: Educational Content
- **Documents**: 5 chapters from organic chemistry textbooks
- **Persona**: Undergraduate Chemistry Student
- **Job**: "Identify key concepts and mechanisms for exam preparation on reaction kinetics"

### Technical Implementation

#### Model Stack (CPU-only, ≤1GB)
- **Embeddings**: MiniLM-L6-v2 (~80MB) - High-quality semantic representations
- **Similarity**: Cosine similarity (sklearn) - Fast, interpretable scoring
- **Summarization**: TextRank (sumy) - Lightweight, extractive summarization

#### Processing Pipeline
1. **Document Processing**: PDF parsing → Section extraction → MongoDB storage
2. **Persona Encoding**: Convert persona + job to semantic embeddings
3. **Section Scoring**: Compute cosine similarity between persona and sections
4. **Content Ranking**: Sort sections by relevance score
5. **Summarization**: Generate refined text using TextRank algorithm

#### Output Format
```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "PhD Researcher in Computational Biology",
    "job_to_be_done": "Prepare literature review",
    "processing_timestamp": "2024-01-01T12:00:00Z",
    "processing_time_seconds": 45.2,
    "total_pdfs_processed": 2,
    "models_used": {
      "embeddings": "MiniLM-L6-v2",
      "similarity": "cosine_similarity",
      "summarization": "TextRank (sumy)"
    }
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "page_number": 3,
      "section_title": "Graph Neural Networks for Molecular Property Prediction...",
      "importance_rank": 1
    }
  ],
  "sub_section_analysis": [
    {
      "document": "doc1.pdf",
      "refined_text": "GNNs are applied in molecular property prediction...",
      "page_number_constraints": {
        "start": 3,
        "end": 4
      }
    }
  ]
}
```

---

## Quick Start Guide

### 1. Build Docker Image
```bash
docker build --platform linux/amd64 -t abode:latest .
```

### 2. Start Backend Server
```bash
docker run --rm -p 8000:8000 -v $(pwd)/abode:/app abode:latest uvicorn abode.app.main:app --host 0.0.0.0 --port 8000
```

### 3. Start Frontend
```bash
cd pdf-frontend
npm install
npm start
```

### 4. Access Application
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

---

## Usage Examples

### Round 1A: PDF Analysis
1. Navigate to "Round 1A: PDF Upload & Analysis"
2. Upload a PDF file
3. View extracted headings, outlines, and summaries
4. Results display automatically after upload

### Round 1B: Persona Intelligence
1. Navigate to "Round 1B: Upload PDFs"
2. Upload 3-10 PDFs for analysis
3. Go to "Round 1B: Persona Analysis"
4. Enter persona and job description
5. Select PDFs and run analysis
6. View ranked relevant sections and summaries

### API Endpoints

#### Round 1A Endpoints
- `POST /ingest/pdf` - Upload and process PDF
- `GET /outline/{pdf_name}` - Get document outline
- `GET /headings/{pdf_name}` - Get detected headings
- `GET /sections/{pdf_name}` - Get document sections
- `GET /summaries/{pdf_name}/{section_id}` - Get section summary

#### Round 1B Endpoints
- `POST /persona-query` - Run persona-driven analysis

---

## Performance & Constraints

### Round 1A Performance
- **Model Size**: ≤200MB (DistilBERT classifier)
- **Processing Time**: ~5-10 seconds per PDF
- **Accuracy**: 96% precision, 100% recall on test set

### Round 1B Performance
- **Model Size**: ≤80MB (MiniLM-L6-v2)
- **Processing Time**: ≤60 seconds for 3-5 documents
- **Scalability**: Handles up to 10 documents efficiently
- **Offline Operation**: No internet access required

---

## File Structure
```
abode/
├─ app/                    # FastAPI backend
│   ├─ main.py            # Main API endpoints
│   ├─ headings_api.py    # Round 1B persona API
│   ├─ db.py              # MongoDB connection
├─ pdf_pipeline/          # Core processing modules
│   ├─ parse_pdf.py       # PDF parsing
│   ├─ heading_detection.py # Heading detection
│   ├─ persona_encoder.py # Round 1B persona encoding
│   ├─ relevance.py       # Round 1B similarity scoring
│   ├─ summarize.py       # Round 1B summarization
│   ├─ mongo_utils.py     # Database utilities
├─ pdf-frontend/          # React frontend
│   ├─ src/
│   │   ├─ components/    # React components
│   │   ├─ App.jsx        # Main app
├─ uploaded_pdfs/         # Uploaded PDF storage
├─ output/               # Processing results
├─ ground_truth/         # Evaluation data
├─ requirements.txt      # Python dependencies
├─ Dockerfile           # Container configuration
├─ approach_explanation.md # Round 1B methodology
```

---

## Evaluation Results

### Round 1A: Heading Detection
```
english_sample_4.json: Precision=1.00, Recall=1.00
english_sample_5.json: Precision=1.00, Recall=1.00
multilang_sample_2.json: Precision=1.00, Recall=1.00
multilang_sample_5.json: Precision=1.00, Recall=1.00
sample_test_headings.json: Precision=0.86, Recall=1.00

Overall: Precision=0.96, Recall=1.00, F1=0.98
```

### Round 1B: Persona Intelligence
- **Domain Agnostic**: Works across research papers, textbooks, financial reports
- **Persona Diversity**: Supports researchers, students, analysts, journalists
- **Job Flexibility**: Handles literature reviews, exam prep, market analysis
- **Performance**: Meets all constraints (CPU-only, ≤1GB, ≤60s, offline)

---

## Troubleshooting

### Common Issues
1. **Backend not running**: Ensure MongoDB is started and backend server is running
2. **Upload errors**: Check file permissions and PDF format
3. **Model loading**: Models are downloaded at build time, no internet needed at runtime
4. **Memory issues**: System designed for CPU-only operation with minimal memory footprint

### Development Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
cd pdf-frontend
npm install

# Start MongoDB (if not using Docker)
mongod

# Start backend
uvicorn abode.app.main:app --reload

# Start frontend
npm start
```

---

## Credits & Technologies
- **PDF Processing**: PyMuPDF, python-docx, LibreOffice
- **Machine Learning**: Transformers, PyTorch, scikit-learn, sentence-transformers
- **Backend**: FastAPI, Motor, uvicorn
- **Frontend**: React, Tailwind CSS, Axios
- **Infrastructure**: Docker, MongoDB
- **Summarization**: sumy, TextRank algorithm

---

## License
This project is developed for the document intelligence challenge and demonstrates state-of-the-art techniques in PDF processing and persona-driven content analysis. 