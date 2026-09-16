from langchain_google_genai import GoogleGenerativeAIEmbeddings
from settings import settings


def get_embedding_model():
    return GoogleGenerativeAIEmbeddings(
        model=settings.embedding_model,
        google_api_key=settings.google_api_key,
    )