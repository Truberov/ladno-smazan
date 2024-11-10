from pydantic import BaseModel


class GenerateRequest(BaseModel):
    query: str
    session_id: str | None = None
