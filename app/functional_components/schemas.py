from pydantic import BaseModel


class RAGPipelineInputSchema(BaseModel):
    query: str
