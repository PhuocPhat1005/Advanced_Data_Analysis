from fastapi import APIRouter, HTTPException

prescriptive_router = APIRouter(prefix="/prescriptive", tags=["Prescriptive Analysis"])


@prescriptive_router.get("/test", summary="summary")
def get_test():
    try:
        return "Test API"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
