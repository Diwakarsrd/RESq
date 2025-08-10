import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def ai_reply(user_text):
    """Generate AI reply using OpenAI"""
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        print("❌ AI Error:", e)
        return "Sorry, I'm having trouble processing your request."
