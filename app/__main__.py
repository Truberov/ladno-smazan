"""Main entrypoint for the app."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.functional_components import get_settings

from app.application.handlers import list_of_routes


def bind_routes(application: FastAPI) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "API for RAG Service"

    application = FastAPI(
        title="RAG Service",
        description=description,
        docs_url="/docs",
        version="1.0.0",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    settings = get_settings()
    bind_routes(application)
    application.state.settings = settings
    return application


app = get_app()

if __name__ == "__main__":
    import uvicorn

    settings_for_application = get_settings()
    uvicorn.run(
        "app.__main__:app",
        host=settings_for_application.app_host,
        port=settings_for_application.app_port,
        log_level="debug",
        reload=False,
    )
