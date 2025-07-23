from fastapi import APIRouter, HTTPException

diagnostic_router = APIRouter(prefix="/diagnostic", tags=["Diagnostic Analysis"])


@diagnostic_router.get("/test", summary="summary")
def get_test():
    try:
        return "Test API"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
