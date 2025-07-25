import fitz

def parse_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    spans = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        try:
            blocks = page.get_text("dict")['blocks']
            for block in blocks:
                if 'lines' not in block:
                    continue
                for line in block['lines']:
                    for span in line['spans']:
                        font_weight = 'bold' if 'Bold' in span['font'] else 'normal'
                        spans.append({
                            'page': page_num + 1,
                            'text': span['text'],
                            'font_name': span['font'],
                            'font_size': span['size'],
                            'font_weight': font_weight,
                            'bbox': span['bbox'],
                        })
        except Exception as e:
            raise Exception(f"Failed to parse page {page_num+1}: {e}")
    return spans 