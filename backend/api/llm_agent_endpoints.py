from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from backend.agent_factory import create_df_agent
from utils.utils import  GLOBAL_DFS, load_csv_to_df, summarize_df
import os
from dotenv import load_dotenv

load_dotenv()

assert "GOOGLE_API_KEY" in os.environ, "Vui lòng set GOOGLE_API_KEY"

llm_agent_router = APIRouter(
    prefix="/llm_agent",
    tags=["dataframe_agent"],
    responses={404: {"description": "Not found"}}
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


@llm_agent_router.post("/ask")
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

    # Tạo agent và ask
    agent = create_df_agent(dfs, req.model)
    answer = agent.invoke(prompt)
    return {"answer": answer}


@llm_agent_router.post("/upload")
async def upload(req: UploadRequest):
    df = load_csv_to_df(req.name, req.csv_content)
    return {"name": req.name, "summary": summarize_df(df)}

