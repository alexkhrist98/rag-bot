import os
from typing import Callable

from langchain.embeddings.ollama import OllamaEmbeddings

OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "ollama-server")

def get_embedding_function() -> Callable:
    return OllamaEmbeddings(
        base_url=OLLAMA_BASE_URL
    )