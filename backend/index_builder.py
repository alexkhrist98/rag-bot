import os

from langchain.schema import Document
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter

from backend.database.chroma_service import ChromaService


class IndexBuilder:
    DATA_DIR = os.getenv("DATA_DIR", "./data")

    def __init__(self):
        self.database: ChromaService = ChromaService()
        self.loader: PyPDFDirectoryLoader = PyPDFDirectoryLoader(self.DATA_DIR)
        self.splitter: CharacterTextSplitter = CharacterTextSplitter()

    def build_index(self) -> None:
        docs = self._prepare_docs()
        chunks = self._split_into_chunks(docs)
        chunk_ids = self._create_chunk_ids(chunks)
        self.database.add_chunks(chunks=chunks, chunk_ids=chunk_ids)

    def _prepare_docs(self) -> list[Document]:
        return self.loader.load()

    def _split_into_chunks(self, docs: list[Document]) -> list[Document]:
        return self.splitter.split_documents(docs)

    def _create_chunk_ids(chunks: list[Document]) -> list[str]:
        chunk_ids = []
        chunk_number = 0
        current_page = 1
        for chunk in chunks:
            chunk_page = chunk.metadata.get("page")
            chunk_source = chunk.metadata.get("source")
            if current_page != chunk_page:
                chunk_number = 0

            chunk_id_string = f"{chunk_source}:{chunk_page}:{chunk_number}"
            chunk_ids.append(chunk_id_string)

        return chunk_ids
