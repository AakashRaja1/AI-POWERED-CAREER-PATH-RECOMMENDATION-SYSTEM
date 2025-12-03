from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Simple chatbot endpoint that processes user messages.
    TODO: Integrate with actual AI/LLM service for career guidance.
    """
    try:
        message = request.message.lower()
        
        # Simple rule-based responses (replace with actual AI integration)
        if "career" in message or "job" in message:
            reply = "I can help you explore various career paths! Based on your skills and interests, I recommend taking our career assessment form. What specific career field interests you?"
        elif "skill" in message:
            reply = "Developing skills is crucial for career growth. Consider focusing on both technical skills (like programming, data analysis) and soft skills (communication, leadership). What skills would you like to develop?"
        elif "certification" in message or "course" in message:
            reply = "Certifications can boost your career! Popular options include AWS, Google Cloud, CFA, PMP, and industry-specific certifications. What field are you interested in?"
        elif "trend" in message or "market" in message:
            reply = "Current job market trends show high demand for AI/ML engineers, data scientists, cloud architects, and cybersecurity specialists. The tech sector continues to grow rapidly!"
        elif "hello" in message or "hi" in message:
            reply = "Hello! I'm your AI Career Assistant. I can help with career guidance, skill recommendations, and job market insights. How can I assist you today?"
        else:
            reply = f"I understand you're asking about: '{request.message}'. I can help with career paths, skills development, certifications, and job market trends. Could you be more specific about what you'd like to know?"
        
        return ChatResponse(reply=reply)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")
