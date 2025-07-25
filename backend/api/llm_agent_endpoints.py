import asyncio
import os
from typing import List

import pandas as pd
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.agent_factory import create_df_agent
from utils.utils import GLOBAL_DFS, DEFAULT_DFS_NAMES, load_csv_to_df, summarize_df

load_dotenv()
assert "GOOGLE_API_KEY" in os.environ, "Vui lòng set GOOGLE_API_KEY"

llm_agent_router = APIRouter(prefix="/llm_agent", tags=["LLM Agent"])


class AskRequest(BaseModel):
    model: str
    prompt_type: str
    custom_prompt: str = ""
    preset_key: str = ""
    user_query: str = ""
    df_names: List[str]


class UploadRequest(BaseModel):
    df_name: str
    csv_content: str


@llm_agent_router.post("/ask", summary="Gửi câu hỏi tới LLM Agent")
async def ask(req: AskRequest):
    # 1. Chuẩn bị instruction (hướng dẫn agent) dựa trên prompt_type
    preset_map = {
        "overview": "Bạn là chuyên gia phân tích dữ liệu. Hãy tóm tắt thống kê chung của DataFrame đã upload.",
        "compare": "Bạn là chuyên gia phân tích dữ liệu. Hãy so sánh dữ liệu giữa các DataFrame đã upload về số lượng, cột và thống kê.",
    }
    if req.prompt_type == "custom":
        instruction = req.custom_prompt.strip()
    elif req.prompt_type == "preset":
        if req.preset_key not in preset_map:
            raise HTTPException(400, detail=f"preset_key không hợp lệ: {req.preset_key}")
        instruction = preset_map[req.preset_key]
    else:
        instruction = "Bạn là chuyên gia phân tích dữ liệu. Hãy tự động gợi ý các phân tích tiềm năng dựa trên DataFrame đã upload."

    if not req.user_query.strip():
        raise HTTPException(400, detail="`user_query` không được để trống.")

    # 2. Kết hợp instruction với câu hỏi thực của user
    full_prompt = f"{instruction}\n\nYêu cầu của người dùng: {req.user_query.strip()}"

    # 3. Lấy DataFrame từ GLOBAL_DFS
    try:
        dfs = [GLOBAL_DFS[name] for name in req.df_names]
    except KeyError as e:
        raise HTTPException(400, detail=f"DataFrame không tồn tại: {e}")

    # 4. Invoke agent trong executor để tránh block
    loop = asyncio.get_running_loop()
    max_retries = 3
    delay = 2  # seconds
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            answer = await loop.run_in_executor(
                None,
                lambda: create_df_agent(dfs, 0.0, req.model).invoke(full_prompt)
            )
            # Nếu thành công, break
            break
        except Exception as e:
            last_err = e
            err_msg = str(e)
            # Nếu lỗi 503 model overloaded, retry
            if "503" in err_msg or "overloaded" in err_msg.lower():
                if attempt < max_retries:
                    await asyncio.sleep(delay * attempt)
                    continue
            # Không retry với lỗi khác
            raise HTTPException(500, detail=f"LLM Agent error: {e}")
    else:
        # Sau hết retry vẫn lỗi
        raise HTTPException(503, detail=f"Model overloaded sau {max_retries} lần thử: {last_err}")

    return {"answer": answer["output"]}


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
    except pd.errors.EmptyDataError as e:
        # pandas ném lỗi khi CSV rỗng
        raise HTTPException(
            status_code=400,
            detail=f"CSV rỗng hoặc không có dữ liệu: {e}"
        )
    except ValueError as e:
        # load_csv_to_df có thể ném ValueError khi decode base64
        raise HTTPException(
            status_code=400,
            detail=f"Không thể decode base64: {e}"
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


@llm_agent_router.get(
    "/defaults",
    summary="Lấy danh sách DataFrame gốc và summary"
)
async def get_defaults():
    """
    Trả về JSON list các object {name, summary} cho từng DataFrame gốc.
    """
    try:
        return [
            {"name": name, "summary": summarize_df(GLOBAL_DFS[name])}
            for name in DEFAULT_DFS_NAMES
        ]
    except Exception as e:
        raise HTTPException(500, detail=f "Error khi lấy defaults: {e}")
