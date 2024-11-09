from fastapi import status, APIRouter

from app.buisness_logic import GenerateRequest
from app.buisness_logic import assistant

api_router = APIRouter(tags=["rag"])


@api_router.post(
    "/ask",
    status_code=status.HTTP_200_OK,
)
async def generate(
        generation_data: GenerateRequest,
):
    return await assistant.reply(generation_data.dict())
