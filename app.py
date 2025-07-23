import uvicorn
from fastapi import FastAPI

from backend.api.descriptive_analysis_endpoints import descriptive_router
from backend.api.diagnostic_analysis_endponts import diagnostic_router
from backend.api.predictive_analysis_endpoints import predictive_router
from backend.api.prescriptive_analysis_endpoints import prescriptive_router

run_app = FastAPI(
    title="Data Analysis Application",
    description="API for Data Analysis Application",
    version="25.1",
)

# Register router
run_app.include_router(descriptive_router)
run_app.include_router(diagnostic_router)
run_app.include_router(predictive_router)
run_app.include_router(prescriptive_router)

if __name__ == "__main__":
    uvicorn.run("app:run_app", host="127.0.0.1", port=8000, reload=True)
