import logging
import os

from langchain.schema import Document
from langchain_gigachat import GigaChat

from backend.database.chroma_service import ChromaService
from backend.llms.functions import get_base64_credentials

class PromptProcessor:
    GIGACHAT_CLIENT_ID = os.getenv("GIGACHAT_CLIENT_ID")
    GIGACHAT_CLIENT_SECRET = os.getenv("GIGACHAT_CLIENT_SECRET")
    def __init__(self):
        self.database:ChromaService = ChromaService()
        self.GIGACHAT_ACCESS_KEY = get_base64_credentials(self.GIGACHAT_CLIENT_ID, self.GIGACHAT_CLIENT_SECRET)
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
        
        return response.content
    
    def _enrich_prompt(self, text:str, context:list[Document]) -> str:
        return f"Дай ответ на запрос основываясь на контексте. В ответе дай ссылки на те места в контексте, которые ты используешь. Контекст: {context}\n запрос: {text}"