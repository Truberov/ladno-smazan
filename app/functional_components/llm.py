from langchain_openai import ChatOpenAI

from .settings import Settings


def get_llm_model(settings: Settings) -> ChatOpenAI:
    return ChatOpenAI(
        model_name=settings.openai_model_name,
        temperature=settings.openai_temperature,
        openai_api_key=settings.openai_api_key,
        openai_api_base=settings.openai_api_base,
    )
