from fastapi import status, APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from app.buisness_logic.documents import process_documents


api_router = APIRouter(tags=["rag"])


@api_router.post(
    "/documents",
    status_code=status.HTTP_200_OK,
)
async def add_documents(
        files: list[UploadFile] = File(...),
):
    """
    Upload multiple documents endpoint.

    Args:
        files: List of files to be processed

    Returns:
        JSONResponse with status of operation
    """
    try:
        # Здесь мы можем добавить валидацию файлов, например:
        for file in files:
            if not file.filename.endswith(('.txt', '.pdf', '.doc', '.docx')):
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"message": f"Unsupported file type: {file.filename}"}
                )

        # Прочитаем содержимое файлов
        documents = []
        for file in files:
            content = await file.read()
            documents.append({
                "filename": file.filename,
                "content": content,
                "content_type": file.content_type
            })


        await process_documents(documents)

        return {
            "message": "Files successfully uploaded",
            "processed_files": [doc["filename"] for doc in documents]
        }

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"An error occurred: {str(e)}"}
        )
