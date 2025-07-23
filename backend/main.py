import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic_settings import BaseSettings
from starlette.middleware.cors import CORSMiddleware

from backend.api import descriptive_analysis_endpoints as da_endpoints

class Settings(BaseSettings):
    APP_TITLE: str = "Data Analysis Application"
    APP_DESC: str = "API for Data Analysis Application"
    APP_VERSION: str = "25.1"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = True
    CORS_ORIGINS: list[str] = ["*"]

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

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "ok"}

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors(), "body": exc.body},
        )

    app.include_router(da_endpoints.da_router, prefix="/analysis", tags=["Analysis"])
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
