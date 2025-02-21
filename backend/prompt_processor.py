import os

from langchain_community.llms.ollama import Ollama

from backend.database.chroma_service import ChromaService

class PromptProcessor:
    MODEL = os.getenv("MODEL", "t5-samll")
    def __init__(self):
        self.database:ChromaService = ChromaService()
        self.llm: Ollama = Ollama(model=self.MODEL)
    
    async def aprocess_prompt(self, text:str) -> str:
        return f"Текст после процессинга:\n {text}"