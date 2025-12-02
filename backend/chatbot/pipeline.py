from .agent import CareerChatAgent
from .training_embed import embed_text
from .training_store import search_chunks

ACTIVE_USERS = {}

def get_agent(user_id):
    if user_id not in ACTIVE_USERS:
        ACTIVE_USERS[user_id] = CareerChatAgent()
    return ACTIVE_USERS[user_id]

def chatbot_answer(user_id, message):
    agent = get_agent(user_id)

    # Search book knowledge
    query_emb = embed_text(message)
    results = search_chunks(query_emb)

    book_context = ""
    if results and "documents" in results:
        book_context = "\n".join(results["documents"][0])

    final_input = f"""
BOOK EXTRACT:
{book_context}

USER QUESTION:
{message}
"""

    return agent.ask(final_input)
