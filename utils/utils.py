import os, glob
import pandas as pd
import base64
from io import StringIO

GLOBAL_DFS: dict[str, pd.DataFrame] = {}

from common import ROOT_PATH
DATA_DIR = os.path.join(ROOT_PATH, "data")

# Duyệt qua tất cả .csv trong thư mục data/
for csv_path in glob.glob(os.path.join(DATA_DIR, "*.csv")):
    name = os.path.basename(csv_path)  # ví dụ "Products_Revenue.csv"
    try:
        df = pd.read_csv(csv_path)
        GLOBAL_DFS[name] = df
        print(f"[utils] Loaded default DataFrame: {name} ({df.shape[0]}×{df.shape[1]})")
    except Exception as e:
        print(f"[utils] Error loading {name}: {e}")

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
