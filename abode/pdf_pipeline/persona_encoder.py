from sentence_transformers import SentenceTransformer
import numpy as np

# Load MiniLM model (CPU only)
_model = None
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cpu')
    return _model

def encode_persona_job(text: str) -> np.ndarray:
    """
    Encode a persona/job description into a semantic embedding.
    Args:
        text (str): Persona and job description.
    Returns:
        np.ndarray: Embedding vector.
    """
    model = get_model()
    embedding = model.encode(text)
    return embedding 