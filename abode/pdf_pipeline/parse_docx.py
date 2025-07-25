import os
import subprocess
import tempfile
from docx import Document

def parse_docx(pdf_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = tmpdir
        cmd = [
            'libreoffice', '--headless', '--convert-to', 'docx', '--outdir', out_dir, pdf_path
        ]
        subprocess.run(cmd, check=True)
        docx_name = os.path.splitext(os.path.basename(pdf_path))[0] + '.docx'
        docx_path = os.path.join(out_dir, docx_name)
        doc = Document(docx_path)
        spans = []
        page = 1  # DOCX doesn't have pages, so set all to 1
        for para in doc.paragraphs:
            style = para.style.name if para.style else ''
            font_name = para.runs[0].font.name if para.runs and para.runs[0].font.name else 'Unknown'
            font_size = para.runs[0].font.size.pt if para.runs and para.runs[0].font.size else 12.0
            font_weight = 'bold' if any(run.bold for run in para.runs) else 'normal'
            spans.append({
                'page': page,
                'text': para.text,
                'font_name': font_name,
                'font_size': font_size,
                'font_weight': font_weight,
                'bbox': None,
                'style': style
            })
        return spans 