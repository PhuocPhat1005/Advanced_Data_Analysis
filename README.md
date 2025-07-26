# Advanced_Data_Analyst
Final Project for Course Data_Analysis

Đầu tiên tạo file .env và set biến `GOOGLE_API_KEY = "your_google_api_key"`
Sau đó, chạy server ở thư mục chính (cao nhất) bằng lệnh :

```python
 uvicorn app:app --reload --port 8000
 ```
Cuối cùng, test frontend bằng chạy lệnh:

```bash
cd test
streamlit run app.py
```

---

## 🚀 Yêu cầu hệ thống
- Python >= 3.11.9
- pip
- (Khuyến nghị) Virtual environment (venv)
- node v22.14.0 (frontend)
- npm 11.2.0 (frontend)

## 🛠️ Cài đặt

### 1. Clone repository:

```bash
git clone https://github.com/PhuocPhat1005/Advanced_Data_Analysis.git
cd advanced-data-analyst
```

### 2. Tạo môi trường cho server (nếu không dùng file .bat và .sh):
#### 2.1. Tạo virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate   # Windows
```

#### 2.2. Cài đặt thư viện:

```bash
pip install -r requirements.txt
```

### 3. Tạo môi trường cho UI (nếu không dùng file .bat và .sh):
```bash
npm install
npm run build
```

## ▶️ Chạy ứng dụng

### Cách 1. Sử dụng file .bat (Window) và .sh (Linux hoặc Mac):
#### Window:

```bash
start_app.bat
```
#### Linux hoặc MacOS:
```bash
chmod +x start_app.sh
start_app.sh
```

### Cách 2. Sử dụng câu lệnh python:
#### Chạy Server:

```bash
python app.py
```
Hoặc:

```bash
uvicorn app:app --reload
```
Server mặc định sẽ chạy tại:
```bash
http://127.0.0.1:8000
```
#### Chạy UI Server:
```bash
npm run start
```
UI Server mặc định sẽ chạy tại:
```bash
http://localhost:3000
```

## 📘 Swagger UI
Tài liệu API tự động (Swagger):

```bash
http://127.0.0.1:8000/docs
```