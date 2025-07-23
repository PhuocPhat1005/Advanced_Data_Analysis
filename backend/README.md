# 📊 Advanced Data Analyst API

Ứng dụng API dùng FastAPI để phân tích dữ liệu từ CSV, bao gồm doanh thu, số lượng, đánh giá, trạng thái hiển thị...

---

## 🚀 Yêu cầu hệ thống

- Python 3.8+
- pip
- (khuyến nghị) Virtual environment (venv)

---

## 🛠️ Cài đặt

### 1. Clone repository:

```bash
git clone https://github.com/your-username/advanced-data-analyst.git
cd advanced-data-analyst
```

### 2. Tạo virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate   # Windows
```

### 3. Cài đặt thư viện:

```bash
pip install -r requirements.txt
```
## ▶️ Chạy ứng dụng

```bash
python app.py
```
Hoặc:

```bash
uvicorn app:run_app --reload
```
Server mặc định sẽ chạy tại:
```bash
http://127.0.0.1:8000
```
## 📘 Swagger UI
Tài liệu API tự động (Swagger):

```bash
http://127.0.0.1:8000/docs
```
