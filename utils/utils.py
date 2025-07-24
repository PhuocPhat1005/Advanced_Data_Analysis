import base64
import glob
import os
import zipfile
from io import StringIO

import pandas as pd

from common import ROOT_PATH

# GLOBAL_DFS lưu các DataFrame (gốc + upload)
GLOBAL_DFS: dict[str, pd.DataFrame] = {}
# DEFAULT_DFS_NAMES lưu tên các DataFrame gốc đã load khi khởi
DEFAULT_DFS_NAMES: list[str] = []

DATA_DIR = os.path.join(ROOT_PATH, "data")


def unzip_data(zip_path, extract_to):
    try:
        os.makedirs(extract_to, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print("✅ Đã giải nén xong.")
    except Exception as e:
        print(f"Giải nén file không thành công: {e}")


unzip_data(DATA_DIR + "\Product_Recommendation.zip", DATA_DIR)

# 1. Duyệt và load tất cả .csv trong thư mục data/ vào GLOBAL_DFS
for csv_path in glob.glob(os.path.join(DATA_DIR, "*.csv")):
    name = os.path.basename(csv_path)  # ví dụ "Products_Revenue.csv"
    try:
        df = pd.read_csv(csv_path)
        GLOBAL_DFS[name] = df
        DEFAULT_DFS_NAMES.append(name)
        print(f"[utils] Loaded default DataFrame: {name} ({df.shape[0]}×{df.shape[1]})")
    except Exception as e:
        print(f"[utils] Error loading {name}: {e}")


# 2. Hàm user upload CSV

def load_csv_to_df(name: str, content: str) -> pd.DataFrame:
    """
    User upload thêm CSV: decode base64 hoặc raw, convert thành DataFrame,
    rồi lưu vào GLOBAL_DFS[name].
    """
    try:
        decoded = base64.b64decode(content).decode('utf-8')
        buf = StringIO(decoded)
    except Exception:
        buf = StringIO(content)
    df = pd.read_csv(buf)
    GLOBAL_DFS[name] = df
    return df


# 3. Hàm tóm tắt DataFrame

def summarize_df(df: pd.DataFrame) -> str:
    lines = [f"- Shape: {df.shape[0]} rows × {df.shape[1]} cols"]
    lines.append("- Nulls per column:")
    for c in df.columns:
        lines.append(f"  • {c}: {df[c].isna().sum()}")
    lines.append("- Unique per column:")
    for c in df.columns:
        lines.append(f"  • {c}: {df[c].nunique()}")
    lines.append("- Descriptive stats:")
    desc = df.describe(include='all').transpose().round(4)
    for idx, row in desc.iterrows():
        stats = ", ".join([f"{k}={v}" for k, v in row.items()])
        lines.append(f"  • {idx}: {stats}")
    return "\n".join(lines)


# 4. Hàm trả về danh sách mặc định (name + summary) để frontend gọi

def get_default_summaries() -> list[dict]:
    """
    Trả về list các dict {name, summary} cho từng DataFrame gốc.
    """
    result = []
    for name in DEFAULT_DFS_NAMES:
        try:
            summary = summarize_df(GLOBAL_DFS[name])
        except Exception as e:
            summary = f"Error summarizing {name}: {e}"
        result.append({"name": name, "summary": summary})
    return result
