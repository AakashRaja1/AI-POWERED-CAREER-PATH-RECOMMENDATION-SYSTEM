from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .pipeline import chatbot_answer
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    user_id: str
    message: str

@router.post("/chat")
async def chat(req: ChatRequest):
    try:
        logger.info(f"Received chat request from user {req.user_id}: {req.message}")
        reply = chatbot_answer(req.user_id, req.message)
        logger.info(f"Generated reply for user {req.user_id}")
        return {"reply": reply}
    except Exception as e:
        logger.error(f"Error in chatbot: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")
