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

