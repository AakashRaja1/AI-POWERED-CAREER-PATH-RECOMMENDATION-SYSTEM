"""
Training text extractor. It reads source documents such as PDFs and prepares raw text for chatbot knowledge building.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from PyPDF2 import PdfReader

def extract_text(pdf_path: str) -> str:
    """
    Extract all text from a PDF file.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text
