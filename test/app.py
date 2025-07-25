# frontend/app.py

import os
import json
import base64
import requests
import time
import streamlit as st
from datetime import datetime

# --- Cấu hình ---
BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")
HISTORY_FILE = "history/chat_history.json"

st.set_page_config(page_title="📊 Tiki Data Analyzer", layout="wide")

# --- Step 0: Lấy danh sách và summary của các file gốc từ backend ---
@st.cache_data(show_spinner=False)
def load_default_summaries():
    try:
        res = requests.get(f"{BACKEND}/ai_agent/llm_agent/defaults")
        res.raise_for_status()
        data = res.json()  # list of {name, summary}
        return {item["name"]: item["summary"] for item in data}
    except Exception:
        return {}

default_summaries = load_default_summaries()
default_dfs = list(default_summaries.keys())

# --- Sidebar: chọn data gốc để include ---
st.sidebar.title("Chọn DataFrame")
include_defaults = st.sidebar.multiselect(
    "Chọn data mặc định để include:",
    default_dfs,
    default=default_dfs
)

# Nếu chưa có trong session, khởi dict lưu các summary (gốc + upload)
if "dfs" not in st.session_state:
    st.session_state.dfs = {name: default_summaries[name] for name in include_defaults}

# --- Sidebar: upload thêm CSV ---
st.sidebar.markdown("---")
uploaded = st.sidebar.file_uploader(
    "Upload CSV (nhiều file)", type="csv", accept_multiple_files=True
)
if uploaded:
    for f in uploaded:
        raw = f.read().decode("utf-8")
        b64 = base64.b64encode(raw.encode()).decode()
        res = requests.post(
            f"{BACKEND}/ai_agent/llm_agent/upload",
            json={"df_name": f.name, "csv_content": b64}
        )
        if res.ok:
            info = res.json()
            st.sidebar.success(f"Đã tải: {info['name']}")
            st.session_state.dfs[info["name"]] = info["summary"]
        else:
            st.sidebar.error(f"Upload lỗi: {res.text}")

# --- Sidebar: cấu hình model & prompt ---
st.sidebar.markdown("---")
st.sidebar.title("Cài đặt LLM & Prompt")

model_options = [
    "gemini-2.5-pro", "gemini-2.5-flash",
    "gemini-2.5-flash-lite", "gemini-2.0-flash",
    "gemini-2.0-flash-lite"
]
selected_model = st.sidebar.selectbox("Chọn model Gemini", model_options)

prompt_type = st.sidebar.radio("Loại prompt", ["custom", "preset"])
custom_prompt = st.sidebar.text_area("Nhập prompt tuỳ chỉnh") if prompt_type=="custom" else ""
preset_key = st.sidebar.selectbox("Chọn prompt mẫu", ["overview","compare"]) if prompt_type=="preset" else ""

# --- Hiển thị summary của tất cả DataFrame đang include ---
st.markdown("## 📋 Tổng hợp DataFrame")
for name, summary in st.session_state.dfs.items():
    with st.expander(name, expanded=False):
        st.text(summary)

# --- Chat area ---
if "chat" not in st.session_state:
    st.session_state.chat = []

st.markdown("---")
query = st.text_input("Nhập câu hỏi và Enter để gửi:", "")

if query:
    st.session_state.chat.append({"role": "user", "text": query})

    # Gọi API với spinner
    with st.spinner("Agent đang xử lý…"):
        payload = {
            "model": selected_model,
            "prompt_type": prompt_type,
            "custom_prompt": custom_prompt,
            "preset_key": preset_key,
            "user_query": query,
            "df_names": list(st.session_state.dfs.keys())
        }
        res = requests.post(f"{BACKEND}/ai_agent/llm_agent/ask", json=payload)

    if res.ok:
        full_resp = res.json().get("answer", "")
    else:
        full_resp = f"Error: {res.text}"

    # Typing effect
    placeholder = st.empty()
    buf = ""
    for ch in full_resp:
        buf += ch
        placeholder.markdown(f"**Agent:** {buf}")
        time.sleep(0.01)
    st.session_state.chat.append({"role": "assistant", "text": full_resp})

# Render lịch sử chat
st.markdown("## 💬 Lịch sử chat")
for msg in st.session_state.chat:
    prefix = "**Bạn:**" if msg["role"]=="user" else "**Agent:**"
    st.markdown(f"{prefix} {msg['text']}")

# --- Lưu lịch sử ---
if st.button("Lưu lịch sử"):
    os.makedirs("history", exist_ok=True)
    record = {
        "timestamp": datetime.now().isoformat(),
        "model": selected_model,
        "prompt_type": prompt_type,
        "preset_key": preset_key,
        "included_dfs": list(st.session_state.dfs.keys()),
        "chat": st.session_state.chat
    }
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    st.success(f"Đã lưu lịch sử vào `{HISTORY_FILE}`")
