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

## 🛠️ Cài đặt

### 1. Clone repository:

```bash
git clone https://github.com/PhuocPhat1005/Advanced_Data_Analysis.git
cd advanced-data-analyst
```

### 2. Tạo môi trường (nếu không dùng file .bat và .sh):
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


## ▶️ Chạy ứng dụng

### Cách 1. Sử dụng file .bat (Window) và .sh (Linux hoặc Mac):
```bash
start_app.bat # Window
start_app.sh # Linux hoặc Mac
```


### Cách 2. Sử dụng câu lệnh python:

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
## 📘 Swagger UI
Tài liệu API tự động (Swagger):

```bash
http://127.0.0.1:8000/docs
```