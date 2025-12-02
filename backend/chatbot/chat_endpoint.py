from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
import tempfile
from PyPDF2 import PdfReader

router = APIRouter()

# Input model for text queries
class UserQuery(BaseModel):
    message: str

# Connect to Chroma
client = chromadb.PersistentClient(path="./parachute_db")
collection = client.get_collection("parachute_book")

# Local embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Optional: Extract text from PDF resume
def extract_text_from_pdf(file: UploadFile):
    reader = PdfReader(file.file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

@router.post("/query")
async def query_bot(message: str = Form(...), resume: UploadFile | None = None):
    """
    Accepts:
    - message: User input message
    - resume: Optional PDF resume
    """
    user_text = message

    # If resume uploaded, append its text
    if resume:
        resume_text = extract_text_from_pdf(resume)
        user_text += "\n" + resume_text

    # Embed the user query
    query_emb = model.encode(user_text)

    # Fetch all stored embeddings
    stored_docs = collection.get(include=["documents", "embeddings"])
    docs = stored_docs['documents']
    embeddings = stored_docs['embeddings']

    # Compute cosine similarity to find top 5 relevant chunks
    sims = [cosine_similarity(query_emb, np.array(e)) for e in embeddings]
    top_indices = np.argsort(sims)[-5:][::-1]  # top 5 chunks

    top_chunks = [docs[i] for i in top_indices]

    # Generate final career advice (simple rule-based combination)
    advice_text = "\n".join(top_chunks)

    # Format response with roadmap, reasoning, and market demand (basic)
    response = {
        "recommended_career": "Based on your input, the top career options are derived from the book.",
        "roadmap": "1. Identify interests and strengths\n2. Build relevant skills\n3. Gain experience and network",
        "reasoning": advice_text,
        "market_demand": "High demand careers are highlighted based on current trends in the book"
    }

    return response
