from app.functional_components import (
    RAGMultiModalModelPipeline,
    get_llm_model,
    get_retriever,
    get_settings,
    SYSTEM_PROMPT,
)

settings = get_settings()
assistant = RAGMultiModalModelPipeline(
    retriever=get_retriever(settings),
    llm=get_llm_model(settings),
    system_prompt=SYSTEM_PROMPT,
    settings=settings,
)
assistant.build_chain()
