import logging

import os

from langchain.schema import Document
from langchain_community.llms.ollama import Ollama

from backend.database.chroma_service import ChromaService

class PromptProcessor:
    MODEL = os.getenv("MODEL", "smollm")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_URL", "http://ollama-server:11434")
    def __init__(self):
        self.database:ChromaService = ChromaService()
        self.llm: Ollama = Ollama(
            model=self.MODEL,
            base_url=self.OLLAMA_BASE_URL
        )
    
    async def aprocess_prompt(self, text:str) -> str:
        logging.debug(f"start processing prompt {text}")
        relevant_data = await self.database.aget_relevant(text=text)
        enriched_prompt = self._enrich_prompt(text, relevant_data)
        logging.debug("Waiting for the response from LLM")
        response = await self.llm.ainvoke(enriched_prompt)
        logging.debug(response)
        
        return response
    
    def _enrich_prompt(self, text:str, context:list[Document]) -> str:
        return f"Дай ответ на запрос основываясь на контексте. В ответе дай ссылки на те места в контексте, которые ты используешь. Контекст: {context}\n запрос: {text}"