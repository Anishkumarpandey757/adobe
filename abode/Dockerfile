FROM python:3.9-slim

# Set environment variables for CPU-only and offline operation
ENV CUDA_VISIBLE_DEVICES=""
ENV TF_CPP_MIN_LOG_LEVEL="2"
ENV TRANSFORMERS_OFFLINE=1
ENV TORCH_DEVICE=cpu
ENV HF_HUB_OFFLINE=1

# Install system dependencies for PDF processing and build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download and cache all required models during build time (offline operation)
# MiniLM-L6-v2 for Round 1B persona encoding (~80MB)
RUN python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2'); print('MiniLM-L6-v2 model downloaded successfully')"

# Download NLTK data for TextRank summarization
RUN python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); print('NLTK data downloaded successfully')"

# Download DistilBERT for Round 1A heading detection (≤200MB)
RUN python -c "from transformers import AutoTokenizer, AutoModel; tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased'); model = AutoModel.from_pretrained('distilbert-base-uncased'); print('DistilBERT model downloaded successfully')"

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploaded_pdfs output input

# Set permissions
RUN chmod +x /app/run.sh

# Expose port for API
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command: start FastAPI server
CMD ["uvicorn", "abode.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Alternative: Run batch processing for Round 1A
# CMD ["python", "-m", "pdf_pipeline.batch_extract", "--input-dir", "/app/input", "--output-dir", "/app/output"] 