from groq import Groq
from .prompts import SYSTEM_PROMPT
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

class CareerChatAgent:
    def __init__(self):
        self.chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

    def ask(self, user_input):
        self.chat_history.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=self.chat_history
        )

        reply = response.choices[0].message.content
        self.chat_history.append({"role": "assistant", "content": reply})

        return reply
