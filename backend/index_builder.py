import os
import logging

from langchain.schema import Document
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from backend.database.chroma_service import ChromaService


class IndexBuilder:
    DATA_DIR = os.getenv("DATA_DIR", "./data")

    def __init__(self):
        self.database: ChromaService = ChromaService()
        self.loader: PyPDFDirectoryLoader = PyPDFDirectoryLoader(self.DATA_DIR)
        self.splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=450
        )

    def build_index(self) -> None:
        docs = self._prepare_docs()
        chunks = self._split_into_chunks(docs)
        chunk_ids = self._create_chunk_ids(chunks)
        logging.info(f"Current number of documents: {len(docs)} containing {len(chunks)} chunks")
        chunks_to_add = self._find_new_chunks(chunks, chunk_ids)
        if len(chunks_to_add) > 0:
            for portion_chunks, portion_ids in zip(self._chunk_iterator(chunks, 25), self._chunk_iterator(chunk_ids, 25)):
                self.database.add_chunks(chunks=portion_chunks, chunk_ids=portion_ids)
        logging.info(f"Processed {len(chunks)}, added: {len(chunks_to_add)}")

    def _prepare_docs(self) -> list[Document]:
        return self.loader.load()

    def _split_into_chunks(self, docs: list[Document]) -> list[Document]:
        return self.splitter.split_documents(docs)

    def _create_chunk_ids(self, chunks: list[Document]) -> list[str]:
        chunk_ids = []
        chunk_number = 0
        current_page = 0
        for chunk in chunks:
            chunk_page = chunk.metadata.get("page")
            chunk_source = chunk.metadata.get("source")
            if current_page != chunk_page:
                chunk_number = 0
                current_page = chunk_page

            chunk_id_string = f"{chunk_source}:{chunk_page}:{chunk_number}"
            chunk.metadata["id"] = chunk_id_string
            chunk_ids.append(chunk_id_string)
            chunk_number += 1

        return chunk_ids
    
    def _chunk_iterator(self, lst: list, chunk_size: int):
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]

    def _find_new_chunks(self, chunks: list[Document], chunks_ids:list[str]) -> list[Document]:
        stored_chunks = self.database.get_stored_chunks()
        stored_chunk_ids = set(stored_chunks["ids"])
        chunk_ids_to_load = set(chunks_ids)
        new_chunks = chunk_ids_to_load.difference(stored_chunk_ids)
        return list(filter(
            lambda chunk : chunk.metadata.get("id") in new_chunks,
            chunks
        ))