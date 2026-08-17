# src/csv_agent/utils.py

import pandas as pd
import plotly
from io import BytesIO


def inspect_dataframe(df: pd.DataFrame) -> dict:
    """
    生成 DataFrame 的详细探查报告（供 AI 理解和前端展示）
    返回一个包含 schema 文本和统计信息的字典
    """
    if df.empty:
        return {"schema_str": "数据为空", "head_str": "", "info": {}}

    # 1. 生成列信息表格（增强版：加上唯一值样例，帮助AI理解内容）
    schema_data = {
        '列名': df.columns,
        '非空数量': df.count().values,
        '空值占比': (df.isnull().mean() * 100).round(2).values,
        '数据类型': df.dtypes.values.astype(str),
        '唯一值样例': [df[col].astype(str).unique()[:3].tolist() for col in df.columns]
    }
    schema_df = pd.DataFrame(schema_data)
    # 转为带格式的字符串，发给AI时更清晰
    schema_str = schema_df.to_string(index=False)

    # 2. 获取前5行数据样本
    head_str = df.head(5).to_string()

    # 3. 额外统计信息（可选）
    info = {
        "行数": len(df),
        "列数": len(df.columns),
        "内存占用(MB)": round(df.memory_usage(deep=True).sum() / (1024 ** 2), 2)
    }

    return {
        "schema_str": schema_str,
        "head_str": head_str,
        "info": info
    }


def load_csv_safely(uploaded_file) -> pd.DataFrame:
    """
    安全读取CSV，自动探测编码（解决中文乱码问题）
    支持从 Streamlit 的 UploadedFile 对象或文件路径读取
    """
    # 如果传入的是文件路径字符串
    if isinstance(uploaded_file, str):
        file_path = uploaded_file
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
        for enc in encodings:
            try:
                return pd.read_csv(file_path, encoding=enc)
            except UnicodeDecodeError:
                continue
        raise ValueError("所有常见编码尝试失败，请检查文件格式")

    # 如果传入的是 Streamlit 的 UploadedFile 对象
    else:
        # 先读取字节流，尝试解码
        content = uploaded_file.getvalue()
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
        for enc in encodings:
            try:
                # 用 BytesIO 模拟文件对象
                return pd.read_csv(BytesIO(content), encoding=enc)
            except UnicodeDecodeError:
                continue
        raise ValueError("无法解码该CSV文件，请确认文件格式为UTF-8或GBK编码")


def capture_exec_output(code: str, df: pd.DataFrame) -> tuple:
    """
    安全执行 AI 生成的代码，并捕获输出（图表对象 或 print内容）
    返回: (result_object, error_message)
    """
    # 准备执行环境
    local_vars = {
        "df": df,
        "pd": pd,
        "plotly": plotly
    }

    # 劫持 print 函数，捕获输出文本
    captured_text = []

    def fake_print(*args, **kwargs):
        captured_text.extend([str(arg) for arg in args])

    local_vars["print"] = fake_print

    try:
        # 执行代码
        exec(code, {}, local_vars)

        # 优先返回图表对象
        if "fig" in local_vars and local_vars["fig"] is not None:
            return local_vars["fig"], None

        # 如果有 print 捕获的内容，返回文本
        if captured_text:
            return "\n".join(captured_text), None

        # 如果代码执行了但既没图也没print，检查是否定义了 df_result
        if "df_result" in local_vars:
            return local_vars["df_result"], None

        return "代码执行成功（无输出结果）", None

    except Exception as e:
        # 把报错信息和生成的代码一起返回，方便调试
        error_msg = f"执行报错: {repr(e)}\n--- 生成的代码 ---\n{code}"
        return None, error_msg