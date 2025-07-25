import os
import argparse
from pdf_pipeline.parse_pdf import parse_pdf
from pdf_pipeline.parse_docx import parse_docx
from pdf_pipeline.heading_detection import detect_headings
import json

def process_pdf(pdf_path):
    try:
        spans = parse_pdf(pdf_path)
    except Exception:
        spans = parse_docx(pdf_path)
    outline = detect_headings(spans, os.path.basename(pdf_path))
    return outline

def main(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for fname in os.listdir(input_dir):
        if fname.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, fname)
            outline = process_pdf(pdf_path)
            out_path = os.path.join(output_dir, os.path.splitext(fname)[0] + '.json')
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(outline, f, ensure_ascii=False, indent=2)
            print(f"Processed {fname} -> {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_input = os.path.abspath(os.path.join(script_dir, '..', 'uploaded_pdfs'))
    default_output = os.path.abspath(os.path.join(script_dir, '..', 'output'))
    parser.add_argument('--input_dir', default=default_input, help=f'Directory with input PDFs (default: {default_input})')
    parser.add_argument('--output_dir', default=default_output, help=f'Directory for output JSONs (default: {default_output})')
    args = parser.parse_args()
    main(args.input_dir, args.output_dir) 