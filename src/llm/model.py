from langchain_openai import ChatOpenAI
from src.config import settings

def get_llm():
    return ChatOpenAI(
        model=settings.MODEL_NAME,
        api_key=settings.DASHSCOPE_API_KEY,
        base_url=settings.BASE_URL,
        temperature=0.7
    )