from pdf2image import convert_from_bytes

from .retriever import MilvusColbertRetriever


class MilvusDataloader:
    def __init__(self, retriever_client: MilvusColbertRetriever):
        self._retriever_client = retriever_client

    def load_document(self, doc: bytes) -> None:
        pass

    def load_documents(self, docs: list[bytes]) -> None:
        pass


