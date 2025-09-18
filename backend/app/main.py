from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Attack Capital AI Backend", version="0.1.0")

    # CORS for frontend dev
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    from app.routes.token import router as token_router  # local import to avoid issues during settings init

    app.include_router(token_router)

    @app.get("/health")
    def health_check():  # pragma: no cover - trivial endpoint
        return {"status": "ok"}

    return app


app = create_app()


