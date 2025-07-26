from pymongo import MongoClient

def get_db(mongo_uri, db_name):
    client = MongoClient(mongo_uri)
    return client[db_name], client

def insert_spans(spans, pdf_name, mongo_uri, db_name):
    db, client = get_db(mongo_uri, db_name)
    for span in spans:
        span['pdf_name'] = pdf_name
        db.spans.insert_one(span)
    client.close()

def insert_outline(outline, pdf_name, mongo_uri, db_name):
    db, client = get_db(mongo_uri, db_name)
    outline_doc = {'pdf_name': pdf_name, 'outline': outline}
    db.outlines.insert_one(outline_doc)
    client.close()

def get_outline(pdf_name, mongo_uri, db_name):
    db, client = get_db(mongo_uri, db_name)
    doc = db.outlines.find_one({'pdf_name': pdf_name})
    client.close()
    if doc:
        return doc['outline']
    return []

def insert_sections(sections, pdf_name, mongo_uri, db_name):
    db, client = get_db(mongo_uri, db_name)
    for section in sections:
        section['pdf_name'] = pdf_name
        db.sections.insert_one(section)
    client.close() 