"""Stage 1 and 2: load the source text, and split it into chunks.

YOUR CODE GOES HERE. Both functions below raise NotImplementedError.
You saw working versions of both in Session 2's `aimakerspace/text_utils.py`:
read it, understand it, then write your own. Copying it verbatim is allowed;
not being able to explain it is not.

Neither function knows or cares what your corpus is about. That is the point:
swap the .txt in data/ and nothing in this file should need to change.
"""

from pathlib import Path


def load_corpus(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()



def split_corpus(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    chunks = []

    range_step = chunk_size - chunk_overlap
    ranges = range(0, len(text), range_step)

    for start in ranges:
        # #1. 0 -> 1000
        # #2. 800 -> 1800
        chunks.append(text[start:start + chunk_size])
    return chunks