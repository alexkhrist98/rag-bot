import logging
import os

from langchain.schema import Document
from langchain_gigachat import GigaChat

from backend.database.chroma_service import ChromaService

class PromptProcessor:
    GIGACHAT_ACCESS_KEY = os.getenv("GIGACHAT_AUTH_KEY") + "=="
    def __init__(self):
        self.database:ChromaService = ChromaService()
        self.llm: GigaChat = GigaChat(
            credentials=self.GIGACHAT_ACCESS_KEY,
            verify_ssl_certs=False,
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