import uvicorn
from fastapi import FastAPI

from api import descriptive_analysis_endpoints as da_endpoints

app1 = FastAPI(
    title="Data Analysis Application",
    description="API for Data Analysis Application",
    version="25.1",
)

# Register router
app1.include_router(da_endpoints.da_router)

if __name__ == "__main__":
    uvicorn.run("main:app1", host="127.0.0.1", port=8000, reload=True)
