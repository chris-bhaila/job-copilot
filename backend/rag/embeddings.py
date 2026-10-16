"""
Wraps the embedding model used for resume + JD matching.
Uses a small, fast, local model via sentence-transformers --
no API calls, no cost, runs fine on CPU.
"""

from sentence_transformers import SentenceTransformer

_MODEL_NAME = "all-MiniLM-L6-v2"
_model = None


def get_model():
    """Lazy-load so importing this module doesn't pull the model into
    memory immediately (keeps tests/imports fast)."""
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of strings. Returns plain lists (Chroma expects
    lists, not numpy arrays)."""
    model = get_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return vectors.tolist()