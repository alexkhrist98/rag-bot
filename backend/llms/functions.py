import os
from typing import Callable

from langchain.embeddings.ollama import OllamaEmbeddings

OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "ollama-server")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-minilm")

def get_embedding_function() -> Callable:
    return OllamaEmbeddings(
        base_url=OLLAMA_BASE_URL,
        model=EMBEDDING_MODEL,
    )