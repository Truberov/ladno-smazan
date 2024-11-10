from fastapi import UploadFile
from pdf2image import convert_from_bytes

from .converter import DocumentConverter
from .generation import retriever


async def process_documents(documents: list[UploadFile]) -> None:
    converter = DocumentConverter()
    _docs = [doc.read() for doc in documents]
    converted_documents = converter.convert_documents(_docs)
    for doc in converted_documents:
        load_document(doc)


def load_document(document: bytes) -> None:
    input_item = convert_from_bytes(document)
    retriever.add_to_index(input_item, store_collection_with_index=True)
