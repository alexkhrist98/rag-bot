import os

from langchain.schema import Document
from langchain_chroma.vectorstores import Chroma

from backend.llms.functions import get_embedding_function

class ChromaService:
    CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma")
    EMBEDDING_FUNCTION = get_embedding_function()

    def __init__(self):
        self.db:Chroma = Chroma(
            embedding_function=self.EMBEDDING_FUNCTION,
            persist_directory=self.CHROMA_DIR,
        )
    
    async def aget_relevant(self, text:str) -> list[Document]:
        return await self.db.asimilarity_search_with_score(text, k=5)
    
    def add_chunks(self, chunks: list[Document], chunk_ids:list):
        return self.db.add_documents(
            documents=chunks,
            ids=chunk_ids,
        )
    
    def get_stored_chunks(self) -> list[str]:
        return self.db.get(include=[])
