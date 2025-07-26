from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load MiniLM model (CPU only)
_model = None
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cpu')
    return _model

def encode_sections(section_texts):
    """
    Encode a list of section texts into embeddings.
    Args:
        section_texts (List[str]): List of section texts.
    Returns:
        np.ndarray: Embedding matrix.
    """
    model = get_model()
    return model.encode(section_texts)

def score_sections(persona_embedding, section_embeddings):
    """
    Compute cosine similarity scores between persona embedding and section embeddings.
    Args:
        persona_embedding (np.ndarray): Embedding for persona/job.
        section_embeddings (np.ndarray): Embeddings for sections.
    Returns:
        np.ndarray: Similarity scores.
    """
    scores = cosine_similarity([persona_embedding], section_embeddings)[0]
    return scores 