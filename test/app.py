import os, json, base64, requests
import streamlit as st
from datetime import datetime

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")
HISTORY_FILE = "history/chat_history.json"

st.set_page_config(page_title="📊 Tiki Data Analyzer", layout="wide")

# Sidebar: chọn model & prompt
model_options = [
    "gemini-2.5-pro", "gemini-2.5-flash",
    "gemini-2.5-flash-lite", "gemini-2.0-flash",
    "gemini-2.0-flash-lite"
]
st.sidebar.title("Cài đặt chung")
selected_model = st.sidebar.selectbox("Chọn Google Gemini model", model_options)

prompt_type = st.sidebar.radio(
    "Chọn loại prompt", ["custom", "preset", "suggest"]
)
if prompt_type == "custom":
    custom_prompt = st.sidebar.text_area("Nhập prompt tuỳ chỉnh")
else:
    custom_prompt = ""
if prompt_type == "preset":
    preset_options = {
        "overview": "Tóm tắt data chung",
        "compare": "So sánh các DataFrame",
        # thêm key nếu cần
    }
    preset_key = st.sidebar.selectbox("Chọn prompt mẫu", list(preset_options.keys()))
else:
    preset_key = ""

# File uploader
st.sidebar.markdown("---")
uploaded = st.sidebar.file_uploader(
    "Upload CSV (nhiều file)", type="csv", accept_multiple_files=True
)

if uploaded:
    if "dfs" not in st.session_state:
        st.session_state.dfs = {}
    for f in uploaded:
        raw = f.read().decode("utf-8")
        b64 = base64.b64encode(raw.encode()).decode()
        res = requests.post(f"{BACKEND}/upload", json={"name": f.name, "csv_content": b64})
        if res.ok:
            info = res.json()
            st.sidebar.success(f"Đã tải: {info['name']}")
            st.session_state.dfs[info["name"]] = info["summary"]
        else:
            st.sidebar.error(f"Upload lỗi: {res.text}")

# Hiển thị summary mỗi DF
if st.session_state.get("dfs"):
    for n, s in st.session_state.dfs.items():
        with st.expander(f"Summary: {n}"):
            st.text(s)

# Chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Nhập câu hỏi
query = st.text_input("Nhập câu hỏi và Enter để gửi:", "")
if query:
    # Add user message
    st.session_state.chat.append({"role": "user", "text": query})
    # Gọi API ask
    payload = {
        "model": selected_model,
        "prompt_type": prompt_type,
        "custom_prompt": custom_prompt,
        "preset_key": preset_key,
        "df_names": list(st.session_state.dfs.keys())
    }
    res = requests.post(f"{BACKEND}/ask", json=payload)
    if res.ok:
        resp = res.json()["answer"]
    else:
        resp = f"Error: {res.text}"
    # Add agent message
    st.session_state.chat.append({"role": "assistant", "text": resp})

# Render chat
for msg in st.session_state.chat:
    if msg["role"] == "user":
        st.markdown(f"**Bạn:** {msg['text']}")
    else:
        st.markdown(f"**Agent:** {msg['text']}")

# Lưu lịch sử ra file JSON
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
    st.success("Đã lưu lịch sử vào history/chat_history.json")
