"""
Chroma vector store: turns resume_data.py into retrievable chunks,
persists them to disk, and exposes retrieval for the matcher.
"""

from pathlib import Path
import chromadb

from .resume_data import SKILLS, EXPERIENCE, PROJECTS, EDUCATION
from .embeddings import embed_texts

_PERSIST_DIR = Path(__file__).resolve().parent.parent / "data" / "chroma"
_COLLECTION_NAME = "resume_chunks"

_client = None
_collection = None


def _get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=str(_PERSIST_DIR))
    return _client


def _build_chunks():
    """
    One chunk per project/experience entry (not per-bullet), so a
    retrieval returns enough context to draft a grounded bullet rather
    than a single dangling sentence.
    """
    chunks = []

    for exp in EXPERIENCE:
        text = (
            f"{exp['title']} at {exp['org']} ({exp['period']}).\n"
            + "\n".join(f"- {b}" for b in exp["bullets"])
        )
        chunks.append({"id": exp["id"], "text": text,
                        "metadata": {"type": "experience", "name": exp["title"]}})

    for proj in PROJECTS:
        text = (
            f"Project: {proj['name']}. Stack: {', '.join(proj['stack'])}.\n"
            + "\n".join(f"- {b}" for b in proj["bullets"])
        )
        chunks.append({"id": proj["id"], "text": text,
                        "metadata": {"type": "project", "name": proj["name"]}})

    # Skills as their own chunk too -- a JD line like "experience with
    # Docker" should match the skills list even if no bullet names it.
    skills_text = "Skills:\n" + "\n".join(
        f"{category}: {', '.join(items)}" for category, items in SKILLS.items()
    )
    chunks.append({"id": "skills", "text": skills_text,
                    "metadata": {"type": "skills", "name": "Skills"}})

    edu_text = (
        f"{EDUCATION['degree']} from {EDUCATION['institution']} ({EDUCATION['status']}).\n"
        f"Coursework: {', '.join(EDUCATION['coursework'])}"
    )
    chunks.append({"id": "education", "text": edu_text,
                    "metadata": {"type": "education", "name": "Education"}})

    return chunks


def build_index(force: bool = False):
    """Embed all resume chunks into Chroma. Safe to call repeatedly --
    skips rebuilding unless force=True or the collection is empty."""
    client = _get_client()
    collection = client.get_or_create_collection(_COLLECTION_NAME)

    if collection.count() > 0 and not force:
        return collection

    if force and collection.count() > 0:
        existing_ids = collection.get()["ids"]
        if existing_ids:
            collection.delete(ids=existing_ids)

    chunks = _build_chunks()
    ids = [c["id"] for c in chunks]
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    embeddings = embed_texts(texts)

    collection.add(ids=ids, documents=texts, metadatas=metadatas, embeddings=embeddings)
    return collection


def get_collection():
    global _collection
    if _collection is None:
        _collection = build_index()
    return _collection


def retrieve(query: str, top_k: int = 3):
    """Retrieve the top_k most relevant resume chunks for a query
    (e.g. a single JD requirement like '3+ years with Docker').
    Returns a list of {id, text, metadata, distance}."""
    collection = get_collection()
    query_embedding = embed_texts([query])[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    return [
        {
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        }
        for i in range(len(results["ids"][0]))
    ]