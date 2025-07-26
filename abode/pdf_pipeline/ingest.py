import argparse
import os
from pdf_pipeline.parse_pdf import parse_pdf
from pdf_pipeline.parse_docx import parse_docx
from pdf_pipeline.mongo_utils import insert_spans, insert_outline, insert_sections
from pdf_pipeline.heading_detection import detect_headings


def extract_sections(spans, outline):
    """
    Group spans into sections based on outline headings.
    Returns a list of section dicts with section_id, level, text, page_start, page_end.
    """
    if not outline or not outline.get('outline'):
        return []
    headings = outline['outline']
    sections = []
    current_section = None
    section_id = 0
    for i, heading in enumerate(headings):
        section_id += 1
        start_page = heading['page']
        end_page = headings[i+1]['page']-1 if i+1 < len(headings) else max(s['page'] for s in spans)
        # Collect all spans between start_page and end_page
        section_spans = [s for s in spans if start_page <= s['page'] <= end_page]
        section_text = '\n'.join(s['text'] for s in section_spans)
        sections.append({
            'section_id': f"{section_id}",
            'level': heading['level'],
            'text': section_text,
            'page_start': start_page,
            'page_end': end_page
        })
    return sections


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
        # --- New: Extract and insert sections ---
        sections = extract_sections(spans, outline)
        insert_sections(sections, pdf_name, args.mongo_uri, args.db)

if __name__ == "__main__":
    main() 