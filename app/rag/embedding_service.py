import google.generativeai as genai

from app.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
client = genai


def generate_embedding(text: str) -> list[float]:
    """
    Generates an embedding for a single semantic chunk.
    """

    response = client.embed_content(
        model="gemini-embedding-2",
        content=text
    )

    return response['embedding']


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generates embeddings for multiple semantic chunks.
    """

    embeddings = []
    for text in texts:
        response = client.embed_content(
            model="gemini-embedding-2",
            content=text
        )
        embeddings.append(response['embedding'])
    
    return embeddings
