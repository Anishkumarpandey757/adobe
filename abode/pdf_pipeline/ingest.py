import argparse
import os
from pdf_pipeline.parse_pdf import parse_pdf
from pdf_pipeline.parse_docx import parse_docx
from pdf_pipeline.mongo_utils import insert_spans, insert_outline
from pdf_pipeline.heading_detection import detect_headings


def main():
    parser = argparse.ArgumentParser(description="Intelligent PDF Processing Pipeline")
    parser.add_argument("input", nargs='+', help="Input PDF file(s)")
    parser.add_argument("--mongo-uri", default="mongodb://localhost:27017", help="MongoDB URI")
    parser.add_argument("--db", default="abode", help="MongoDB database name")
    args = parser.parse_args()

    for pdf_path in args.input:
        pdf_name = os.path.basename(pdf_path)
        try:
            spans = parse_pdf(pdf_path)
        except Exception as e:
            print(f"PDF parsing failed for {pdf_path}: {e}. Attempting DOCX fallback...")
            spans = parse_docx(pdf_path)
        insert_spans(spans, pdf_name, args.mongo_uri, args.db)
        outline = detect_headings(spans, pdf_name)
        insert_outline(outline, pdf_name, args.mongo_uri, args.db)

if __name__ == "__main__":
    main() 