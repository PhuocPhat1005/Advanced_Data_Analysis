import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings
from starlette.middleware.cors import CORSMiddleware

from backend.api.descriptive_analysis_endpoints import descriptive_router
from backend.api.diagnostic_analysis_endponts import diagnostic_router
from backend.api.predictive_analysis_endpoints import predictive_router
from backend.api.prescriptive_analysis_endpoints import prescriptive_router
from backend.api.llm_agent_endpoints import llm_agent_router


class Settings(BaseSettings):
    APP_TITLE: str       = "Data Analysis Application"
    APP_DESC: str        = "API for Data Analysis Application"
    APP_VERSION: str     = "25.1"
    HOST: str            = "127.0.0.1"
    PORT: int            = 8000
    RELOAD: bool         = True
    CORS_ORIGINS: list[str] = ["*"]
    GOOGLE_API_KEY: str  # ← thêm biến này

    class Config:
        env_file = ".env"

settings = Settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESC,
        version=settings.APP_VERSION,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors(), "body": exc.body},
        )

    app.include_router(descriptive_router, prefix="/analysis")
    app.include_router(diagnostic_router, prefix="/analysis")
    app.include_router(predictive_router, prefix="/analysis")
    app.include_router(prescriptive_router, prefix="/analysis")
    app.include_router(llm_agent_router, prefix="/ai_agent")
    return app
app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
