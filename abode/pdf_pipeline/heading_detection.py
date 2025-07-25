import numpy as np
import re
from transformers import pipeline

# Load DistilBERT or similar model for heading detection
# You can replace 'distilbert-base-uncased-finetuned-sst-2-english' with your own fine-tuned model
heading_classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

HEADING_LABELS = {"LABEL_1", "HEADING", "heading"}  # Adjust based on your model's output


def is_heading_ml(text, threshold=0.8):
    if not text or len(text) < 4:
        return False
    result = heading_classifier(text)
    label = result[0]['label']
    score = result[0]['score']
    return (label in HEADING_LABELS) and (score > threshold)


def detect_headings(spans, pdf_name):
    from collections import defaultdict
    page_spans = defaultdict(list)
    for span in spans:
        page_spans[span['page']].append(span)
    font_sizes = [span['font_size'] for span in spans if span['font_size']]
    if not font_sizes:
        return {'title': '', 'outline': []}
    size_arr = np.array(font_sizes)
    h1_thresh = np.percentile(size_arr, 90)
    h2_thresh = np.percentile(size_arr, 70)
    h3_thresh = np.percentile(size_arr, 50)
    outline = []
    title = ''
    page1_spans = page_spans.get(1, [])
    if page1_spans:
        max_span = max(page1_spans, key=lambda s: s['font_size'])
        title = max_span['text']
    for span in spans:
        text = span['text'].strip()
        if not text:
            continue
        level = None
        # Heuristic font size
        if span['font_size'] >= h1_thresh:
            level = 'H1'
        elif span['font_size'] >= h2_thresh:
            level = 'H2'
        elif span['font_size'] >= h3_thresh:
            level = 'H3'
        # Regex for numbered or ALL-CAPS
        if re.match(r'^[A-Z\s]{4,}$', text):
            level = level or 'H2'
        if re.match(r'^(\d+\.|[IVXLC]+\.)', text):
            level = level or 'H2'
        # ML-based heading detection
        if is_heading_ml(text):
            if not level:
                level = 'H2'  # Default to H2 if ML says heading but no size/regex match
        if level:
            outline.append({'level': level, 'text': text, 'page': span['page']})
    return {'title': title, 'outline': outline} 