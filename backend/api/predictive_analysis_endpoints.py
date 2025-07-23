from fastapi import APIRouter, HTTPException

predictive_router = APIRouter(prefix="/predictive", tags=["Predictive Analysis"])


@predictive_router.get("/test", summary="summary")
def get_test():
    try:
        return "Test API"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
