import base64
import logging
import os
from typing import Callable

from langchain_gigachat.embeddings import GigaChatEmbeddings
def get_embedding_function() -> Callable:
    return GigaChatEmbeddings(
        credentials=GIGACHAT_ACCESS_KEY,
        verify_ssl_certs=False,
        scope="GIGACHAT_API_PERS"
    )

def get_base64_credentials(client_id:str, client_secret:str) -> str:
    pair_bytes = f"{client_id}:{client_secret}".encode("utf-8")
    return base64.b64encode(pair_bytes).decode("utf-8")
#some sunny day I'll move this to a config object
GIGACHAT_CLIENT_ID = os.getenv("GIGACHAT_CLIENT_ID")
GIGACHAT_CLIENT_SECRET = os.getenv("GIGACHAT_CLIENT_SECRET")
GIGACHAT_ACCESS_KEY = get_base64_credentials(GIGACHAT_CLIENT_ID, GIGACHAT_CLIENT_SECRET)