"""Stage 3 and 4: embed the chunks, store them, and search them.

YOUR CODE GOES HERE. `Hit` and the OpenAI client are written for you, because
plumbing is not the lesson. `embed_texts`, `cosine_similarity`, `build_index`
and `search` are the lesson.
"""

from dataclasses import dataclass

import numpy as np
from openai import OpenAI
from numpy.linalg import norm

EMBEDDING_MODEL = "text-embedding-3-small"

_cached: OpenAI | None = None


def client() -> OpenAI:
    """The OpenAI client, built on first use and reused after that.

    It is built lazily, not at import time, so that .env has already been
    loaded by the time it looks for OPENAI_API_KEY.
    """
    global _cached
    if _cached is None:
        _cached = OpenAI()
    return _cached


@dataclass
class Hit:
    """One retrieved chunk, and everything you need to cite it.

    `chunk_id` is what makes an answer traceable: when an answer is wrong in
    Week 4, this is how you find out which chunk caused it. Keep it.
    """

    chunk_id: int
    text: str
    score: float

    def citation(self) -> str:
        """A short, human-readable label for this chunk. Printed under answers."""
        preview = " ".join(self.text.split())[:60]
        return f"[chunk {self.chunk_id}] {preview}... (score {self.score:.3f})"


def embed_texts(texts: list[str]) -> np.ndarray:
    response = client().embeddings.create(input=texts, model=EMBEDDING_MODEL)
    print(f"Response usage: {response.usage}")
    #Python "list comprehension" setup
    return np.array([item.embedding for item in response.data])


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """How similar are two vectors? 1.0 is identical, 0.0 is unrelated.

    Hint: the dot product, divided by the product of the two norms.
    NumPy has `np.dot` and `np.linalg.norm`.
    """
    return np.dot(a,b) / (norm(a) * norm(b))


def build_index(chunks: list[str]) -> np.ndarray:
    matrix = embed_texts(chunks)
    return np.array(matrix)


def search(query: str, chunks: list[str], matrix: np.ndarray, k: int = 3) -> list[Hit]:
    embedded_query = embed_texts([query])[0]
    score_threshold: float = 0.3
    hits: list[Hit] = [] 

    for i, (chunk, element) in enumerate(zip(chunks, matrix)):
        score = cosine_similarity(embedded_query, element)
        if score > score_threshold:
            # chunk_id is the position in the matrix
            hits.append(Hit(chunk_id=i, text=chunk, score=score))

    return sorted(hits, key=lambda h: h.score, reverse=True)[:k]

