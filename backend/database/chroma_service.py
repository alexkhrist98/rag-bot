import os

from langchain.schema import Document
from langchain_chroma.vectorstores import Chroma

class ChromaService:
    CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma")

    def __init__(self):
        self.db:Chroma = Chroma()._persist_directory(self.CHROMA_DIR)
    
    async def aget_relevant(self, text:str) -> list[Document]:
        return await self.db.asimilarity_search(text)
    
    def add_chunks(self, chunks: list[Document], chunk_ids:list):
        return self.db.add_documents(
            documents=chunks
            ids=chunk_ids
        )
