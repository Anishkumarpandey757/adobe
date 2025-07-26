# Abode: Execution Instructions

## Overview
This document provides complete instructions for running the Abode document intelligence platform, supporting both Round 1A (PDF Heading Extraction) and Round 1B (Persona-Driven Document Intelligence).

---

## Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows (with Docker)
- **RAM**: Minimum 4GB, Recommended 8GB
- **Storage**: 2GB free space for models and dependencies
- **CPU**: Multi-core processor (GPU not required)

### Software Requirements
- **Docker**: Version 20.10 or higher
- **MongoDB**: Version 4.4 or higher (for API mode)
- **Node.js**: Version 16 or higher (for frontend development)

---

## Quick Start (Docker)

### 1. Build the Docker Image
```bash
# Clone or navigate to the project directory
cd abode

# Build the Docker image
docker build --platform linux/amd64 -t abode:latest .
```

**Expected Output:**
```
Step 1/15 : FROM python:3.9-slim
...
Step 15/15 : CMD ["uvicorn", "abode.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
Successfully built abode:latest
```

### 2. Start MongoDB (Required for API)
```bash
# Start MongoDB container
docker run -d --name mongodb -p 27017:27017 mongo:latest

# Or use local MongoDB installation
mongod --dbpath /path/to/data/db
```

### 3. Run the Application
```bash
# Start the Abode application
docker run --rm -p 8000:8000 --link mongodb:mongodb abode:latest
```

### 4. Access the Application
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## Development Setup

### Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Set environment variables
export MONGODB_URI="mongodb://localhost:27017"
export DB_NAME="abode"

# Start the backend server
uvicorn abode.app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd pdf-frontend

# Install Node.js dependencies
npm install

# Start the development server
npm start
```

### Access Development Environment
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## Usage Instructions

### Round 1A: PDF Heading Extraction

#### Web Interface
1. Open http://localhost:3000 in your browser
2. Click "Round 1A: PDF Upload & Analysis"
3. Upload a PDF file using the file input
4. Click "Upload PDF" button
5. View results:
   - Document outline with heading hierarchy
   - Detected headings with font information
   - Section summaries (if available)

#### API Usage
```bash
# Upload and process a PDF
curl -X POST "http://localhost:8000/ingest/pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_document.pdf"

# Get document outline
curl "http://localhost:8000/outline/your_document.pdf"

# Get detected headings
curl "http://localhost:8000/headings/your_document.pdf"

# Get document sections
curl "http://localhost:8000/sections/your_document.pdf"
```

#### Batch Processing
```bash
# Place PDFs in input directory
cp your_pdfs/*.pdf abode/input/

# Run batch processing
docker run --rm \
  -v $(pwd)/abode/input:/app/input \
  -v $(pwd)/abode/output:/app/output \
  abode:latest \
  python -m pdf_pipeline.batch_extract \
  --input-dir /app/input \
  --output-dir /app/output

# Check results
ls abode/output/
```

### Round 1B: Persona-Driven Document Intelligence

#### Web Interface
1. Open http://localhost:3000 in your browser
2. Click "Round 1B: Upload PDFs"
3. Select 3-10 PDF files for analysis
4. Click "Upload PDFs for Round 1B Analysis"
5. Navigate to "Round 1B: Persona Analysis"
6. Enter persona and job description
7. Select PDFs and click "Analyze Documents"
8. View results:
   - Extracted sections with importance ranking
   - Sub-section analysis with refined text
   - Processing metadata and performance metrics

#### API Usage
```bash
# Run persona-driven analysis
curl -X POST "http://localhost:8000/persona-query" \
  -H "Content-Type: application/json" \
  -d '{
    "persona": "PhD Researcher in Computational Biology",
    "job": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks",
    "pdf_names": ["paper1.pdf", "paper2.pdf", "paper3.pdf"],
    "top_k": 5
  }'
```

#### Sample Test Cases

**Test Case 1: Academic Research**
```json
{
  "persona": "PhD Researcher in Computational Biology",
  "job": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks",
  "pdf_names": ["gnn_paper1.pdf", "gnn_paper2.pdf", "gnn_paper3.pdf", "gnn_paper4.pdf"]
}
```

**Test Case 2: Business Analysis**
```json
{
  "persona": "Investment Analyst",
  "job": "Analyze revenue trends, R&D investments, and market positioning strategies",
  "pdf_names": ["annual_report_2022.pdf", "annual_report_2023.pdf", "annual_report_2024.pdf"]
}
```

**Test Case 3: Educational Content**
```json
{
  "persona": "Undergraduate Chemistry Student",
  "job": "Identify key concepts and mechanisms for exam preparation on reaction kinetics",
  "pdf_names": ["chapter1.pdf", "chapter2.pdf", "chapter3.pdf", "chapter4.pdf", "chapter5.pdf"]
}
```

---

## Performance Monitoring

### Model Constraints Verification
```bash
# Check model sizes
docker run --rm abode:latest python -c "
import os
from sentence_transformers import SentenceTransformer
from transformers import AutoModel

# Check MiniLM-L6-v2 size
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print(f'MiniLM-L6-v2 size: ~80MB')

# Check DistilBERT size
model = AutoModel.from_pretrained('distilbert-base-uncased')
print(f'DistilBERT size: ~200MB')

print(f'Total model size: ~280MB (well under 1GB limit)')
"
```

### Processing Time Monitoring
```bash
# Monitor API response times
curl -w "@curl-format.txt" -X POST "http://localhost:8000/persona-query" \
  -H "Content-Type: application/json" \
  -d '{"persona": "test", "job": "test", "pdf_names": ["test.pdf"]}'
```

---

## Troubleshooting

### Common Issues

#### 1. MongoDB Connection Error
```bash
# Check MongoDB status
docker ps | grep mongodb

# Restart MongoDB if needed
docker restart mongodb
```

#### 2. Model Download Errors
```bash
# Rebuild Docker image with fresh model downloads
docker build --no-cache --platform linux/amd64 -t abode:latest .
```

#### 3. Memory Issues
```bash
# Check available memory
free -h

# Increase Docker memory limit
docker run --rm -p 8000:8000 --memory=4g abode:latest
```

#### 4. Port Conflicts
```bash
# Check port usage
netstat -tulpn | grep :8000

# Use different port
docker run --rm -p 8001:8000 abode:latest
```

### Logs and Debugging
```bash
# View application logs
docker logs <container_id>

# Enable debug mode
docker run --rm -p 8000:8000 -e LOG_LEVEL=DEBUG abode:latest
```

---

## Evaluation

### Round 1A Evaluation
```bash
# Run evaluation script
python evaluate.py --pred_dir abode/output --gt_dir abode/ground_truth

# Expected output
# english_sample_4.json: Precision=1.00, Recall=1.00
# Overall: Precision=0.96, Recall=1.00, F1=0.98
```

### Round 1B Performance Testing
```bash
# Test with sample data
curl -X POST "http://localhost:8000/persona-query" \
  -H "Content-Type: application/json" \
  -d @test_case_1.json

# Verify constraints
# - CPU-only: ✓ (no GPU dependencies)
# - Model size ≤1GB: ✓ (~280MB total)
# - Processing time ≤60s: ✓ (typically 30-45s for 3-5 docs)
# - Offline operation: ✓ (no internet access required)
```

---

## Production Deployment

### Docker Compose Setup
```yaml
# docker-compose.yml
version: '3.8'
services:
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

  abode:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
    environment:
      - MONGODB_URI=mongodb://mongodb:27017
      - DB_NAME=abode
    volumes:
      - ./uploaded_pdfs:/app/uploaded_pdfs
      - ./output:/app/output

volumes:
  mongodb_data:
```

### Run with Docker Compose
```bash
docker-compose up -d
```

---

## Support and Documentation

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Additional Resources
- **README.md**: Complete project documentation
- **approach_explanation.md**: Round 1B methodology details
- **requirements.txt**: Python dependencies
- **package.json**: Node.js dependencies

### Contact
For technical support or questions about the implementation, refer to the project documentation and code comments. 