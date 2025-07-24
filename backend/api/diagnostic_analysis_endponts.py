import json
import os
from typing import List

from fastapi import APIRouter, HTTPException, UploadFile, File, Header
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from process_data.diagnostic_analysis.PoorRatingAnalysis import PoorRatingAnalysis
from process_data.diagnostic_analysis.StatusDiagnosticAnalysis import StatusDiagnosticAnalysis
from utils.utils import GLOBAL_DFS

diagnostic_router = APIRouter(prefix="/diagnostic", tags=["Diagnostic Analysis"])


class AnalyzeReasonRequest(BaseModel):
    factor_groups: List[str] = Field(..., description="Danh sách các nhóm phân tích.")
    min_date: str = Field("2016-01-01", description="Ngày bắt đầu lọc (YYYY-MM-DD), VD: 2016-01-01")
    max_date: str = Field(..., description="Ngày kết thúc lọc (YYYY-MM-DD), VD: 2020-01-03.")


@diagnostic_router.post("/rating", summary="Phân tích xếp hạng của sản phẩm.")
def analyze(request: AnalyzeReasonRequest):
    try:
        result = PoorRatingAnalysis().analyze(
            GLOBAL_DFS["Rating_RootCause.csv"],
            rating_col="rating_average",
            factor_groups=request.factor_groups,
            date_column="date_created",
            min_date=request.min_date,
            max_date=request.max_date
        )
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"rating_reason.json"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        return FileResponse(
            path=file_path,
            media_type="application/json",
            filename="rating_reason.json"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@diagnostic_router.post("/rating/llm", summary="Giải thích lý do dựa trên LLM.")
async def analyze_reason_by_llm(
        file: UploadFile = File(..., description="File JSON đầu vào."),
        api_key: str = Header(..., description="API key để gọi LLM.", alias="X-API-Key")
):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file JSON.")

    try:
        contents = await file.read()
        json_data = json.loads(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi đọc file JSON: {str(e)}")

    try:
        result = PoorRatingAnalysis().analyze_reason(reason_json=json_data, api_key=api_key)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@diagnostic_router.post("/status", summary="Phân tích trạng thái của sản phẩm.")
def analyze_status(request: AnalyzeReasonRequest):
    try:
        result = StatusDiagnosticAnalysis().diagnostic_analysis(
            GLOBAL_DFS["Status_RootCause.csv"],
            target_col="status",
            factor_groups=request.factor_groups,
            date_column="date_created",
            min_date=request.min_date,
            max_date=request.max_date
        )
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"status_reason.json"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        return FileResponse(
            path=file_path,
            media_type="application/json",
            filename="status_reason.json"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@diagnostic_router.post("/status/llm", summary="Giải thích lý do dựa trên LLM.")
async def explain_status_by_llm(
        file: UploadFile = File(..., description="File JSON đầu vào."),
        api_key: str = Header(..., description="API key để gọi LLM.", alias="X-API-Key")
):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file JSON.")

    try:
        contents = await file.read()
        json_data = json.loads(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi đọc file JSON: {str(e)}")

    try:
        result = StatusDiagnosticAnalysis().analyze_reason(reason_json=json_data, api_key=api_key)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
