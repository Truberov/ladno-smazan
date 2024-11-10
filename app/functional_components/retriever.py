from byaldi import RAGMultiModalModel

from .settings import Settings


def get_retriever(settings: Settings) -> RAGMultiModalModel:
    return RAGMultiModalModel.from_index(
        index_path=settings.retriever_index_name,
        index_root=settings.retriever_index_root,
        device='cuda'
    )
