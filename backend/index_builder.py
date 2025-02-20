from backend.database.chroma_service import ChromaService

class IndexBuilder:
    def __init__(self):
        self.database:ChromaService = ChromaService()
    
    def build_index(self):
        pass