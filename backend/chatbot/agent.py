"""
Career chatbot orchestration module. It combines retrieved knowledge, prompt rules, and the Groq client to produce career-focused answers for users.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from .prompts import SYSTEM_PROMPT
from .groq_client import get_groq_client

class CareerChatAgent:
    def __init__(self):
        self.chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.question_count = 0

    def ask(self, user_input):
        self.chat_history.append({"role": "user", "content": user_input})

        client = get_groq_client()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=self.chat_history
        )

        reply = response.choices[0].message.content
        self.chat_history.append({"role": "assistant", "content": reply})

        if "?" in reply:
            self.question_count += 1

        return reply
