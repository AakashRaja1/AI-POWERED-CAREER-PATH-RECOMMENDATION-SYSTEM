from sentence_transformers import SentenceTransformer

# Load a free pre-trained embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text: str):
    """
    Generate embeddings for a text chunk using sentence-transformers (local, free).
    """
    embedding = model.encode(text)
    return embedding.tolist()  # convert to list for storing in Chroma
