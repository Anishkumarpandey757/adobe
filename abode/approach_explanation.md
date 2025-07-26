# Round 1B: Persona-Driven Document Intelligence - Approach Explanation

## Methodology Overview

Our system implements a **persona-driven document intelligence pipeline** that extracts and prioritizes relevant sections from 3-10 PDF documents based on specific personas and their job-to-be-done requirements. The approach follows a **semantic similarity-based ranking** methodology using state-of-the-art NLP models while maintaining CPU-only operation and strict performance constraints.

## Technical Approach

### 1. Document Processing Pipeline
- **PDF Parsing**: Uses PyMuPDF (fitz) for robust text extraction with font and layout information
- **Section Extraction**: Groups text spans by detected headings (H1/H2/H3) using font size heuristics and ML-based classification
- **MongoDB Storage**: Stores structured document data (spans, outlines, sections) for efficient retrieval

### 2. Persona & Job Understanding
- **Semantic Encoding**: Converts persona and job descriptions into dense vector representations using **MiniLM-L6-v2** (80MB model)
- **Context Fusion**: Combines persona and job into a single semantic query: `"{persona}. {job}"`
- **CPU Optimization**: All embeddings computed on CPU with efficient batch processing

### 3. Section Relevance Scoring
- **Semantic Embedding**: Each document section is encoded using the same MiniLM-L6-v2 model
- **Cosine Similarity**: Computes similarity scores between persona/job embedding and all section embeddings
- **Ranking**: Sorts sections by relevance score in descending order

### 4. Content Summarization
- **TextRank Algorithm**: Uses sumy library for extractive summarization of top-ranked sections
- **Sentence Selection**: Extracts 2 most important sentences per section
- **Fallback Mechanism**: If summarization fails, uses first two sentences as refined text

## Model Stack & Constraints

### Models Used:
- **Embeddings**: MiniLM-L6-v2 (~80MB) - CPU-friendly, high-quality semantic representations
- **Similarity**: Cosine similarity (sklearn) - Fast, interpretable scoring
- **Summarization**: TextRank (sumy) - Lightweight, extractive summarization

### Performance Compliance:
- **CPU-only**: All models run on CPU with no GPU dependencies
- **Model size ≤1GB**: Total model footprint ~80MB (well under limit)
- **Processing time ≤60s**: Optimized for 3-5 documents, scales to 10 documents
- **Offline operation**: No internet access required during execution

## Output Format

The system produces structured JSON output with:
1. **Metadata**: Input documents, persona, job, timestamp, processing time
2. **Extracted Sections**: Document, page number, section title, importance rank
3. **Sub-section Analysis**: Document, refined text, page number constraints

## Generalization Capability

The solution is **domain-agnostic** and handles diverse inputs:
- **Documents**: Research papers, textbooks, financial reports, news articles
- **Personas**: Researchers, students, analysts, journalists, entrepreneurs
- **Jobs**: Literature reviews, exam preparation, market analysis, content summarization

The semantic approach ensures robust performance across different domains and document types while maintaining the required performance constraints. 