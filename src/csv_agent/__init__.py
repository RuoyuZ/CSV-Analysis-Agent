# src/csv_agent/__init__.py

"""
CSV Analysis Agent - 基于自然语言的数据分析包
"""

# 把核心类直接暴露在包顶层，方便导入
from .agent import CSVAnalysisAgent
# 把常用的工具函数也暴露出来，方便调试
from .utils import inspect_dataframe, load_csv_safely

# 定义公开接口列表，限制 from csv_agent import * 的导入范围
__all__ = [
    "CSVAnalysisAgent",
    "inspect_dataframe",
    "load_csv_safely",
]

# 可以定义版本号，方便后续维护
__version__ = "0.1.0"