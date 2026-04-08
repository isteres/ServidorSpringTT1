from fastapi import FastAPI

def create_app() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.
    """
    app = FastAPI(
        title="Hexagonal FastAPI",
        description="A REST API following Hexagonal Architecture",
        version="1.0.0"
    )

    # Health check endpoint
    @app.get("/health", tags=["System"])
    def health_check():
        return {"status": "ok", "message": "Service is running"}

    # TODO: Include routers from src.infrastructure.web.controllers here
    # app.include_router(some_router)

    return app

app = create_app()