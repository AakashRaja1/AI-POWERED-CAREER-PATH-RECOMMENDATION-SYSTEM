import os
from .training_extract import extract_text
from .training_embed import embed_text
from .training_store import add_chunk

def train_book(pdf_path: str):
    """
    Full pipeline: extract text, chunk it, embed it, and store in Chroma.
    """
    text = extract_text(pdf_path)

    # Simple chunking (split by ~1000 characters)
    chunk_size = 1000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    for i, chunk in enumerate(chunks):
        emb = embed_text(chunk)
        add_chunk(chunk, metadata={"id": f"chunk_{i}"})
        print(f"Embedding chunk {i+1}/{len(chunks)} done")

    print("Training finished.")
