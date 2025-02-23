import logging

import os
from typing import Callable

from langchain_gigachat.embeddings import GigaChatEmbeddings

GIGACHAT_ACCESS_KEY = os.getenv("GIGACHAT_AUTH_KEY") + "=="
def get_embedding_function() -> Callable:
    return GigaChatEmbeddings(
        credentials=GIGACHAT_ACCESS_KEY,
        verify_ssl_certs=False,
        scope="GIGACHAT_API_PERS"
    )