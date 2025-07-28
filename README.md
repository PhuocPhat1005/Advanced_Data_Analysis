# ĐỒ ÁN CUỐI KỲ : PHÂN TÍCH DỮ LIỆU THÔNG MINH
## PHÁT TRIỂN HỆ THỐNG PHÂN TÍCH DỮ LIỆU TÍCH HỢP LLMs TRÊN TẬP DỮ LIỆU PHỤ KIỆN THỜI TRANG TIKI

Final Project for Course Data_Analysis

Đầu tiên tạo file .env và set biến `GOOGLE_API_KEY = "your_google_api_key"`

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
uvicorn app:app --reload --port 800
```
Server mặc định sẽ chạy tại:
```bash
http://127.0.0.1:8000
```
#### Chạy UI Server:
```bash
cd frontend
npm run build
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

---

# TÀI LIỆU

* GG DRIVE : [link here](https://drive.google.com/drive/folders/1oyUwp31QkCl0z3t0l3Ua4GbochOzat45?usp=sharing)
* VIDEO : [link here](https://youtu.be/p4qmyA-IBH4)

<!-- BEGIN YOUTUBE-CARDS -->
[![Pattern Recognition](https://ytcards.demolab.com/?id=p4qmyA-IBH4&title=Phát+Triển+Hệ+Thống+Phân+Tích+Tự+Động+LLMs&lang=en&timestamp=p4qmyA-IBH4&background_color=%230d1117&title_color=%23ffffff&stats_color=%23dedede&max_title_lines=1&width=250&border_radius=5&duration=716 "Phát triển hệ thống phân tích tự động LLMs")](https://www.youtube.com/watch?v=p4qmyA-IBH4)
<!-- END YOUTUBE-CARDS -->

  
