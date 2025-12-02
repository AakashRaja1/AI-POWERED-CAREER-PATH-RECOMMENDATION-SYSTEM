import chromadb

# Use the new PersistentClient format (Chroma latest version)
client = chromadb.PersistentClient(path="./parachute_db")

# Create or get the collection to store embeddings
collection = client.get_or_create_collection("parachute_book")

def add_chunk(chunk: str, metadata: dict):
    """
    Add a text chunk and its metadata to the Chroma collection.
    """
    collection.add(
        documents=[chunk],
        metadatas=[metadata],
        ids=[metadata.get("id")]
    )

def search_chunks(query_embedding, n_results=5):
    """
    Search for relevant chunks using the query embedding.
    Returns the top n_results most similar chunks.
    """
    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results
    except Exception as e:
        print(f"Error searching chunks: {e}")
        return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
