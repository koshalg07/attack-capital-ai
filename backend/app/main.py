from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Attack Capital AI Backend", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    from app.routes.token import router as token_router  
    from app.routes.agent import router as agent_router
    app.include_router(token_router)
    app.include_router(agent_router)

    @app.get("/health")
    def health_check():  
        return {"status": "ok"}

    return app


app = create_app()


