from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from backend.agent_factory import create_df_agent
from utils.utils import GLOBAL_DFS, load_csv_to_df, summarize_df
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
assert "GOOGLE_API_KEY" in os.environ, "Vui lòng set GOOGLE_API_KEY"

llm_agent_router = APIRouter(
    prefix="/llm_agent",
    tags=["LLM Agent"]
)


class AskRequest(BaseModel):
    model: str
    prompt_type: str
    custom_prompt: str = ""
    preset_key: str = ""
    df_names: List[str]


class UploadRequest(BaseModel):
    df_name: str
    csv_content: str


@llm_agent_router.post(
    "/ask",
    summary="Gửi câu hỏi tới LLM Agent",
    description="Gửi prompt (tùy chỉnh, preset hoặc gợi ý) để LLM phân tích các DataFrame đã upload và trả về kết quả.")
async def ask(req: AskRequest):
    # Chuẩn bị prompt theo loại
    if req.prompt_type == "custom":
        prompt = req.custom_prompt
    elif req.prompt_type == "preset":
        # Map preset_key → câu lệnh
        preset_map = {
            "overview": "Tóm tắt thống kê chung của DataFrame đã upload.",
            "compare": "So sánh dữ liệu giữa các DataFrame đã upload về số lượng, cột, thống kê.",
            # ... thêm khi cần
        }
        prompt = preset_map.get(req.preset_key, "")
    else:  # suggest
        prompt = "Hãy tự động gợi ý các phân tích tiềm năng dựa trên DataFrame đã upload."

    # Lấy các DataFrame
    try:
        dfs = [GLOBAL_DFS[name] for name in req.df_names]
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"DataFrame không tồn tại: {e}")

    # Tạo agent và hỏi
    agent = create_df_agent(dfs, req.model)
    answer = agent.invoke(prompt)
    return {"answer": answer}


@llm_agent_router.post(
    "/upload",
    summary="Upload và tóm tắt DataFrame",
    description="Nhận CSV string từ client, chuyển thành DataFrame, lưu vào GLOBAL_DFS và trả về tóm tắt (summary).")
async def upload(req: UploadRequest):
    df = load_csv_to_df(req.df_name, req.csv_content)
    summary = summarize_df(df)
    return {"name": req.df_name, "summary": summary}
