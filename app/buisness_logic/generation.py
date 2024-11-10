from app.functional_components import (
    RAGMultiModalModelPipeline,
    Agent,
    get_llm_model,
    get_retriever,
    get_settings,
    RAG_SYSTEM_PROMPT,
    AGENT_PROMPT_TEMPLATE,
)

settings = get_settings()
retriever = get_retriever(settings)
llm = get_llm_model(settings)

rag_pipeline = RAGMultiModalModelPipeline(
    retriever=retriever,
    llm=llm,
    system_prompt=RAG_SYSTEM_PROMPT,
    settings=settings,
)
rag_pipeline.build_chain()

agent = Agent(
    llm=llm,
    system_prompt=AGENT_PROMPT_TEMPLATE,
    rag_pipeline=rag_pipeline,
)
agent.build_agent()
