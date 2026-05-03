"""
Embedding helper for chatbot knowledge. It converts text chunks into vectors that can be searched later during chat.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from sentence_transformers import SentenceTransformer

# Load a free pre-trained embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text: str):
    """
    Generate embeddings for a text chunk using sentence-transformers (local, free).
    """
    embedding = model.encode(text)
    return embedding.tolist()  # convert to list for storing in Chroma
