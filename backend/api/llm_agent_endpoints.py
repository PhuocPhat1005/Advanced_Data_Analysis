from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import os, asyncio
from dotenv import load_dotenv

# Nếu utils ở trong backend/
from backend.agent_factory import create_df_agent
from utils.utils import GLOBAL_DFS, load_csv_to_df, summarize_df

load_dotenv()
assert "GOOGLE_API_KEY" in os.environ, "Vui lòng set GOOGLE_API_KEY"

llm_agent_router = APIRouter(prefix="/llm_agent", tags=["LLM Agent"])

class AskRequest(BaseModel):
    model: str
    prompt_type: str
    custom_prompt: str = ""
    preset_key: str = ""
    df_names: List[str]

class UploadRequest(BaseModel):
    df_name: str
    csv_content: str

@llm_agent_router.post("/ask", summary="Gửi câu hỏi tới LLM Agent")
async def ask(req: AskRequest):
    # 1. Chuẩn bị prompt
    preset_map = {
        "overview": "Tóm tắt thống kê chung của DataFrame đã upload.",
        "compare": "So sánh dữ liệu giữa các DataFrame đã upload về số lượng, cột, thống kê.",
    }
    if req.prompt_type == "custom":
        prompt = req.custom_prompt
    elif req.prompt_type == "preset":
        if req.preset_key not in preset_map:
            raise HTTPException(400, detail=f"preset_key không hợp lệ: {req.preset_key}")
        prompt = preset_map[req.preset_key]
    else:
        prompt = "Hãy tự động gợi ý các phân tích tiềm năng dựa trên DataFrame đã upload."

    # 2. Lấy DataFrame
    try:
        dfs = [GLOBAL_DFS[name] for name in req.df_names]
    except KeyError as e:
        raise HTTPException(400, detail=f"DataFrame không tồn tại: {e}")

    # 3. Invoke agent trong executor, tránh block
    loop = asyncio.get_running_loop()
    try:
        answer = await loop.run_in_executor(
            None,
            lambda: create_df_agent(dfs, req.model).invoke(prompt)
        )
    except Exception as e:
        raise HTTPException(500, detail=f"LLM Agent error: {e}")

    return {"answer": answer}

@llm_agent_router.post(
    "/upload",
    summary="Upload và tóm tắt DataFrame",
    description="Nhận CSV string từ client, chuyển thành DataFrame, lưu vào GLOBAL_DFS và trả về tóm tắt (summary)."
)
async def upload(req: UploadRequest):
    # 1. Validate input
    if not req.df_name:
        raise HTTPException(status_code=400, detail="`df_name` không được để trống.")
    if not req.csv_content:
        raise HTTPException(status_code=400, detail="`csv_content` không được để trống.")

    # 2. Thử decode & load CSV
    try:
        df = load_csv_to_df(req.df_name, req.csv_content)
    except ValueError as e:
        # load_csv_to_df có thể ném ValueError khi decode base64
        raise HTTPException(
            status_code=400,
            detail=f"Không thể decode base64: {e}"
        )
    except pd.errors.EmptyDataError as e:
        # pandas ném lỗi khi CSV rỗng
        raise HTTPException(
            status_code=400,
            detail=f"CSV rỗng hoặc không có dữ liệu: {e}"
        )
    except pd.errors.ParserError as e:
        # lỗi phân tích cú pháp CSV
        raise HTTPException(
            status_code=400,
            detail=f"Lỗi khi parse CSV: {e}"
        )
    except Exception as e:
        # bất kỳ lỗi nào khác
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error khi load DataFrame: {e}"
        )

    # 3. Tóm tắt DataFrame
    try:
        summary = summarize_df(df)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error khi tóm tắt DataFrame: {e}"
        )

    # 4. Trả về kết quả
    return {
        "name": req.df_name,
        "summary": summary
    }

