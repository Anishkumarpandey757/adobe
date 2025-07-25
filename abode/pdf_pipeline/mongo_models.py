from pymongo import MongoClient, ASCENDING
from pymongo.operations import IndexModel

class Span:
    collection_name = 'spans'
    schema = {
        'pdf_name': str,
        'page': int,
        'text': str,
        'font_name': str,
        'font_size': float,
        'font_weight': str,
        'bbox': list  # [x0, y0, x1, y1]
    }
    @classmethod
    def create_indexes(cls, db):
        db[cls.collection_name].create_index([
            ('pdf_name', ASCENDING),
            ('page', ASCENDING)
        ])

class Outline:
    collection_name = 'outlines'
    schema = {
        'pdf_name': str,
        'title': str,
        'outline': list  # [{level, text, page}]
    }
    @classmethod
    def create_indexes(cls, db):
        db[cls.collection_name].create_index('pdf_name')

class Section:
    collection_name = 'sections'
    schema = {
        'pdf_name': str,
        'section_id': str,
        'level': str,
        'text': str,
        'page_start': int,
        'page_end': int
    }
    @classmethod
    def create_indexes(cls, db):
        db[cls.collection_name].create_index([
            ('pdf_name', ASCENDING),
            ('section_id', ASCENDING)
        ])

class Embedding:
    collection_name = 'embeddings'
    schema = {
        'pdf_name': str,
        'section_id': str,
        'vector': list,  # float array
        'persona_job': str
    }
    @classmethod
    def create_indexes(cls, db):
        # For MongoDB Atlas vector search, you would use a special vector index.
        # Here, we use a placeholder for a 2dsphere index for demonstration.
        db[cls.collection_name].create_index('pdf_name')
        # Example for Atlas: db.embeddings.create_index([('vector', 'vector')])
        # Placeholder for local: db.embeddings.create_index([('vector', '2dsphere')])

class Summary:
    collection_name = 'summaries'
    schema = {
        'pdf_name': str,
        'section_id': str,
        'summary_text': str
    }
    @classmethod
    def create_indexes(cls, db):
        db[cls.collection_name].create_index('pdf_name')

# Example usage to create all indexes:
def create_all_indexes(mongo_uri, db_name):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    Span.create_indexes(db)
    Outline.create_indexes(db)
    Section.create_indexes(db)
    Embedding.create_indexes(db)
    Summary.create_indexes(db)
    client.close() 