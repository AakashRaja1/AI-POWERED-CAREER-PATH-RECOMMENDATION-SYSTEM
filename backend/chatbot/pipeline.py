from .agent import CareerChatAgent
from .groq_client import get_groq_client
from app.core.config import settings
import re
import logging
import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

logger = logging.getLogger(__name__)

ACTIVE_USERS = {}
MAX_CHATBOT_QUESTIONS = 5
_MAX_CHAT_MESSAGES = 16
_MAX_BOOK_CONTEXT_CHARS = 1200
_LLM_EXECUTOR = ThreadPoolExecutor(max_workers=4)
_RETRIEVAL_ENABLED = os.getenv("CHAT_RETRIEVAL_ENABLED", "0").lower() in {"1", "true", "yes"}
_RETRIEVAL_IMPORT_ATTEMPTED = False
_embed_text = None
_search_chunks = None


def _get_retrieval_helpers():
    global _RETRIEVAL_IMPORT_ATTEMPTED, _embed_text, _search_chunks

    if not _RETRIEVAL_ENABLED:
        return None, None

    if not _RETRIEVAL_IMPORT_ATTEMPTED:
        _RETRIEVAL_IMPORT_ATTEMPTED = True
        try:
            from .training_embed import embed_text
            from .training_store import search_chunks

            _embed_text = embed_text
            _search_chunks = search_chunks
        except Exception as e:
            logger.info("Chat retrieval unavailable; continuing without book context: %s", e)

    return _embed_text, _search_chunks


def _trim_chat_history(agent):
    # Keep system prompt + most recent messages to control token/latency growth.
    if len(agent.chat_history) <= _MAX_CHAT_MESSAGES:
        return
    system_msg = agent.chat_history[0]
    recent_messages = agent.chat_history[-(_MAX_CHAT_MESSAGES - 1):]
    agent.chat_history = [system_msg] + recent_messages


def _call_groq_chat_completion(client, messages):
    return client.chat.completions.create(
        model=settings.GROQ_CHAT_MODEL,
        messages=messages,
        max_tokens=settings.GROQ_MAX_COMPLETION_TOKENS,
        temperature=0.2,
    )


def _shorten_reply(text: str) -> str:
    cleaned = " ".join((text or "").strip().split())
    if not cleaned:
        return "Please share a little more detail."

    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    reply = " ".join(sentences[:2]).strip()
    words = reply.split()
    if len(words) > 45:
        reply = " ".join(words[:45]).rstrip(" ,;:")
    return reply


def _sanitize_user_visible_reply(text: str) -> str:
    raw = (text or "").strip()
    if not raw:
        return "Please share a little more detail."

    # Remove leaked internal context scaffold if the model echoes it.
    markers = [
        "PREVIOUS QUESTIONS IN CONVERSATION:",
        "INFORMATION PROVIDED BY USER:",
        "BOOK EXTRACT:",
        "USER QUESTION:",
    ]

    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    filtered = []
    for line in lines:
        if any(line.startswith(marker) for marker in markers):
            continue
        # Remove numbered question history lines like "1. ..." after leaked marker blocks.
        if re.match(r"^\d+\.\s+", line):
            continue
        filtered.append(line)

    cleaned = " ".join(filtered).strip()
    return cleaned or "Please share a little more detail."


def _build_conversation_rule(question_count: int) -> str:
    remaining = max(0, MAX_CHATBOT_QUESTIONS - question_count)
    if remaining == 0:
        return (
            "You have already used the maximum of 5 clarifying questions in this conversation. "
            "Do not ask any more questions. Give a direct, short answer in 1 to 3 sentences."
        )
    return (
        f"You may ask at most 1 short clarifying question in this reply. "
        f"You have {remaining} clarifying question(s) left in this conversation. "
        "Prefer answering directly if you can. Keep the reply short."
    )

def get_agent(user_id):
    if user_id not in ACTIVE_USERS:
        ACTIVE_USERS[user_id] = CareerChatAgent()
    return ACTIVE_USERS[user_id]

def extract_previous_questions(chat_history, current_message):
    """Extract previous questions from chat history for reference"""
    # Get all user messages
    user_messages = [msg["content"] for msg in chat_history if msg["role"] == "user"]
    
    logger.info(f"All user messages: {user_messages}")
    logger.info(f"Current message: {current_message}")
    
    # The current message was JUST added to history, so exclude the last message
    # which should be the current message
    if user_messages and user_messages[-1] == current_message:
        previous_messages = user_messages[:-1]
    else:
        # Fallback: exclude by string comparison
        previous_messages = [msg for msg in user_messages if msg != current_message]
    
    logger.info(f"Previous messages after filtering: {previous_messages}")
    
    if not previous_messages:
        return "PREVIOUS QUESTIONS IN CONVERSATION:\n  None (this is the first message)\n\n"
    
    context = "PREVIOUS QUESTIONS IN CONVERSATION:\n"
    for i, msg in enumerate(previous_messages, 1):
        context += f"  {i}. {msg}\n"
    
    context += "\n"
    logger.info(f"Previous questions context: {context}")
    return context

def extract_structured_user_info(chat_history):
    """Extract and structure user information from chat history"""
    # Get ALL user messages from history, EXCLUDING the system message
    user_messages = [msg["content"] for msg in chat_history if msg["role"] == "user"]
    
    logger.info(f"Extracting info from {len(user_messages)} user messages: {user_messages}")
    
    if not user_messages:
        return "INFORMATION PROVIDED BY USER:\n  None yet\n"
    
    # Parse user messages to extract key information
    info = {}
    
    # Look for name patterns in ALL user messages
    for msg in user_messages:
        # Multiple patterns for name extraction
        name_patterns = [
            r"my name is\s+([A-Za-z]+)",  # My name is X
            r"i'm\s+([A-Za-z]+)\b",        # I'm X (word boundary)
            r"i am\s+([A-Za-z]+)\b",       # I am X (word boundary)
            r"name\s+is\s+([A-Za-z]+)",    # name is X
            r"call me\s+([A-Za-z]+)",      # call me X
            r"my name's\s+([A-Za-z]+)",    # my name's X
            r"it's\s+([A-Za-z]+)\b",       # it's X (word boundary)
        ]
        
        # Only extract name if not already found
        if "Name" not in info:
            for pattern in name_patterns:
                match = re.search(pattern, msg, re.IGNORECASE)
                if match:
                    info["Name"] = match.group(1).capitalize()
                    logger.info(f"Found name: {info['Name']} from message: {msg}")
                    break
    
    # Format the information
    context = "INFORMATION PROVIDED BY USER:\n"
    
    # Add structured information first
    if info:
        for key, value in info.items():
            context += f"  {key}: {value}\n"
        logger.info(f"Extracted info: {info}")
    else:
        # If no name found, show all raw user messages to debug
        logger.warning(f"No structured info found. Raw messages: {user_messages}")
        context += "  [Debug] User messages:\n"
        for i, msg in enumerate(user_messages, 1):
            context += f"    {i}. {msg}\n"
    
    return context

def chatbot_answer(user_id, message):
    agent = get_agent(user_id)
    client = get_groq_client()

    # Add current message to chat history FIRST so extraction can see it
    agent.chat_history.append({"role": "user", "content": message})
    _trim_chat_history(agent)

    # Search book knowledge
    embed_text, search_chunks = _get_retrieval_helpers()
    if embed_text and search_chunks:
        try:
            query_emb = embed_text(message)
            results = search_chunks(query_emb, n_results=3)
        except Exception as e:
            logger.warning("Context retrieval failed, continuing without book context: %s", e)
            results = {"documents": [[]]}
    else:
        results = {"documents": [[]]}

    book_context = ""
    if results and "documents" in results:
        book_context = "\n".join(results["documents"][0])[:_MAX_BOOK_CONTEXT_CHARS]

    # Extract structured user information (now includes current message)
    user_info_context = extract_structured_user_info(agent.chat_history)
    
    # Extract previous questions (EXCLUDING the current message)
    previous_questions_context = extract_previous_questions(agent.chat_history, message)

    # Create enriched message with context
    enriched_message = f"""{previous_questions_context}
{user_info_context}
BOOK EXTRACT:
{book_context}

USER QUESTION:
{message}
"""

    # Replace the raw user message with the enriched one for the API call
    # This prevents duplication
    messages_for_api = [
        agent.chat_history[0],
        {"role": "system", "content": _build_conversation_rule(agent.question_count)},
    ] + agent.chat_history[1:-1] + [{"role": "user", "content": enriched_message}]

    # Get response from agent
    future = _LLM_EXECUTOR.submit(_call_groq_chat_completion, client, messages_for_api)
    try:
        response = future.result(timeout=settings.GROQ_REQUEST_TIMEOUT_SECONDS)
        raw_reply = response.choices[0].message.content
        reply = _shorten_reply(_sanitize_user_visible_reply(raw_reply))
    except FuturesTimeoutError:
        logger.warning("Groq request timed out after %.2fs", settings.GROQ_REQUEST_TIMEOUT_SECONDS)
        reply = "I can help quickly. Please ask a short, specific career question and I will reply in one concise step."
    except Exception as e:
        logger.error("Groq request failed: %s", e)
        reply = "I hit a temporary issue generating your answer. Please try again with a shorter message."

    agent.chat_history.append({"role": "assistant", "content": reply})
    if "?" in reply:
        agent.question_count += 1
    _trim_chat_history(agent)

    return reply
