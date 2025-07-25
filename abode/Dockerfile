FROM --platform=linux/amd64 python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libreoffice libreoffice-writer && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download model weights at build time (DistilBERT, <200MB)
RUN python -c "from transformers import pipeline; pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english')"

# Copy all code
COPY . .

# Entrypoint: process all PDFs in /app/input and write JSONs to /app/output
CMD ["python", "pdf_pipeline/batch_extract.py", "--input_dir", "/app/input", "--output_dir", "/app/output"] 