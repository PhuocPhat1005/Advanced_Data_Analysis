import os
import json
import base64
import requests
import time
import streamlit as st
from datetime import datetime

# URL backend (có thể override qua ENV)
BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")
HISTORY_FILE = "history/chat_history.json"

st.set_page_config(page_title="📊 Tiki Data Analyzer", layout="wide")

# --- Sidebar: cấu hình chung ---
st.sidebar.title("Cài đặt chung")

# Chọn model Gemini
model_options = [
    "gemini-2.5-pro", "gemini-2.5-flash",
    "gemini-2.5-flash-lite", "gemini-2.0-flash",
    "gemini-2.0-flash-lite"
]
selected_model = st.sidebar.selectbox("Chọn model Google Gemini", model_options)

# Chọn loại prompt
prompt_type = st.sidebar.radio("Chọn loại prompt", ["custom", "preset", "suggest"])
custom_prompt = ""
preset_key = ""

if prompt_type == "custom":
    custom_prompt = st.sidebar.text_area("Nhập prompt tuỳ chỉnh")
elif prompt_type == "preset":
    preset_key = st.sidebar.selectbox("Chọn prompt mẫu", ["overview", "compare"])

st.sidebar.markdown("---")

# --- Upload CSV ---
uploaded = st.sidebar.file_uploader(
    "Upload CSV (hỗ trợ nhiều file)", type="csv", accept_multiple_files=True
)

if uploaded:
    if "dfs" not in st.session_state:
        st.session_state.dfs = {}
    for f in uploaded:
        raw = f.read().decode("utf-8")
        b64 = base64.b64encode(raw.encode()).decode()
        # Gọi API upload
        res = requests.post(
            f"{BACKEND}/ai_agent/llm_agent/upload",
            json={"df_name": f.name, "csv_content": b64}
        )
        if res.ok:
            info = res.json()
            st.sidebar.success(f"Đã tải: {info['name']}")
            # Lưu summary để render
            st.session_state.dfs[info["name"]] = info["summary"]
        else:
            st.sidebar.error(f"Upload lỗi: {res.text}")

# Hiển thị tóm tắt cho từng DataFrame
if st.session_state.get("dfs"):
    for name, summary in st.session_state.dfs.items():
        with st.expander(f"Summary: {name}"):
            st.text(summary)

st.sidebar.markdown("---")

# --- Chat area ---
if "chat" not in st.session_state:
    st.session_state.chat = []

# Input user
query = st.text_input("Nhập câu hỏi và Enter để gửi:", "")

if query:
    # 1. Append user message
    st.session_state.chat.append({"role": "user", "text": query})

    # 2. Gọi API trong spinner
    with st.spinner("Agent đang suy nghĩ, xin chờ..."):
        payload = {
            "model": selected_model,
            "prompt_type": prompt_type,
            "custom_prompt": custom_prompt,
            "preset_key": preset_key,
            "df_names": list(st.session_state.dfs.keys())
        }
        res = requests.post(f"{BACKEND}/ai_agent/llm_agent/ask", json=payload)

    # 3. Xử lý response
    if res.ok:
        full_resp = res.json().get("answer", "")
    else:
        full_resp = f"Error: {res.text}"

    # 4. Typing effect: placeholder để update dần
    placeholder = st.empty()
    text_buf = ""
    for ch in full_resp:
        text_buf += ch
        placeholder.markdown(f"**Agent:** {text_buf}")
        time.sleep(0.01)  # điều chỉnh tốc độ gõ
    # Sau khi in hết, thêm vào lịch sử
    st.session_state.chat.append({"role": "assistant", "text": full_resp})

# Render toàn bộ lịch sử chat
for msg in st.session_state.chat:
    if msg["role"] == "user":
        st.markdown(f"**Bạn:** {msg['text']}")
    else:
        st.markdown(f"**Agent:** {msg['text']}")

# --- Lưu lịch sử ---
if st.button("Lưu lịch sử"):
    os.makedirs("history", exist_ok=True)
    record = {
        "timestamp": datetime.now().isoformat(),
        "model": selected_model,
        "prompt_type": prompt_type,
        "preset_key": preset_key,
        "chat": st.session_state.chat
    }
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    st.success(f"Đã lưu lịch sử vào `{HISTORY_FILE}`")
