from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # openai_base_url: str
    openai_model_name: str
    openai_temperature: float
    openai_api_key: str

    retriever_index_name: str
    retriever_index_root: str = '.byaldi'
    retriever_top_k: int = 4

    app_port: int = 8080
    app_host: str = '0.0.0.0'

    model_config = SettingsConfigDict()


def get_settings():
    return Settings()
