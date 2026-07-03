from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_embedding(text: str) -> list[float]:
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts
    )

    return [
        embedding.values
        for embedding in response.embeddings
    ]
