from fastapi import status, APIRouter

from app.buisness_logic import GenerateRequest, agent
from app.buisness_logic import rag_pipeline

api_router = APIRouter(tags=["rag"])


@api_router.post(
    "/ask",
    status_code=status.HTTP_200_OK,
)
async def generate(
        generation_data: GenerateRequest,
):
    return await rag_pipeline.reply(generation_data.dict())


@api_router.post(
    "/ask/v2",
    status_code=status.HTTP_200_OK,
)
async def generate(
        generation_data: GenerateRequest,
):
    return await agent.reply(generation_data.dict())
