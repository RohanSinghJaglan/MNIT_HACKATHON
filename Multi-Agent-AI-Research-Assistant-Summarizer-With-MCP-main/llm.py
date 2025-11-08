from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os


load_dotenv()

def get_llm():
    return ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    api_key=os.getenv("api_key")
)