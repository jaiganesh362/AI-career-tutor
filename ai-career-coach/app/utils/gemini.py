import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini 1.5 Flash model (fast + free-tier friendly)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def ask_gemini(prompt: str) -> str:
    """Send prompt to Gemini and return response text."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {e}"
