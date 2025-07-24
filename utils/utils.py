import pandas as pd
import base64
from io import StringIO

# GLOBAL_DFS: lưu tạm các DataFrame đã upload
GLOBAL_DFS = {}

def load_csv_to_df(name: str, content: str) -> pd.DataFrame:
    """
    Chuyển nội dung CSV (raw hoặc base64) về pandas.DataFrame,
    rồi lưu vào GLOBAL_DFS theo key 'name'.
    """
    # Thử decode base64, nếu fail thì coi content là raw CSV
    try:
        decoded = base64.b64decode(content).decode('utf-8')
        buf = StringIO(decoded)
    except Exception:
        buf = StringIO(content)
    df = pd.read_csv(buf)
    GLOBAL_DFS[name] = df
    return df

def summarize_df(df: pd.DataFrame) -> str:
    """
    Tạo summary string cho DataFrame:
    - shape, nulls, uniques
    - describe
    """
    lines = []
    lines.append(f"- Rows × Cols: {df.shape[0]} × {df.shape[1]}")
    lines.append("- Null counts per column:")
    lines += [f"    • {col}: {df[col].isna().sum()}" for col in df.columns]
    lines.append("- Unique counts per column:")
    lines += [f"    • {col}: {df[col].nunique()}" for col in df.columns]
    lines.append("- Descriptive statistics:")
    desc = df.describe(include='all').transpose().round(4)
    for idx, row in desc.iterrows():
        stats = ", ".join([f"{k}={v}" for k, v in row.items()])
        lines.append(f"    • {idx}: {stats}")
    return "\n".join(lines)
