# src/csv_agent/agent.py

import os
from openai import OpenAI
from .utils import inspect_dataframe, capture_exec_output  # 导入工具函数


class CSVAnalysisAgent:
    def __init__(self, api_key=None, model="deepseek-coder", base_url=None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 DEEPSEEK_API_KEY 环境变量或在初始化时传入")

        # 默认 Base URL 指向 DeepSeek
        _base_url = base_url or os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        self.client = OpenAI(api_key=self.api_key, base_url=_base_url)
        self.model = model
        self.df = None
        self._schema_cache = None  # 缓存探查结果

    def load_data(self, df):
        self.df = df
        # 调用 utils 中的探查函数
        self._schema_cache = inspect_dataframe(df)

    def ask(self, user_question):
        if self.df is None or self.df.empty:
            return "请先加载数据！"

        # 构建系统提示词（使用缓存的 schema）
        system_prompt = f"""
        你是一个资深数据分析专家。请根据问题生成 Python 代码操作 df。

        【数据 Schema】
        {self._schema_cache['schema_str']}

        【数据前5行样例】
        {self._schema_cache['head_str']}

        【规则】
        1. 仅返回纯Python代码，不要解释，不要markdown标记。
        2. 如果画图，必须使用 `fig = plotly.express.xxx(...)` 赋值给 fig。
        3. 如果输出表格，请赋值给 `df_result`；如果输出数值，请直接 `print(数值)`。
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            temperature=0.1
        )
        code = response.choices[0].message.content
        code = code.replace("```python", "").replace("```", "").strip()

        # 调用 utils 中的安全执行器
        result, error = capture_exec_output(code, self.df)

        if error:
            return error
        return result