import streamlit as st
import pandas as pd
import plotly
import os
from dotenv import load_dotenv
from csv_agent import CSVAnalysisAgent, load_csv_safely  # 从包导入

load_dotenv()  # 加载 .env 文件

st.set_page_config(layout="wide")
st.title("📊 CSV 智能分析 Agent")

with st.sidebar:
    st.header("⚙️ 配置")

    # 优先从环境变量取，未取到则让用户输入
    default_key = os.getenv("DEEPSEEK_API_KEY", "")
    api_key = st.text_input(
        "DeepSeek API Key",
        value=default_key,
        type="password",
        placeholder="sk-xxxxxxxxxxxxxxxx"
    )

    uploaded_file = st.file_uploader("上传 CSV 文件", type=["csv"])

    if uploaded_file and api_key:
        try:
            # 使用安全加载函数（自动处理编码）
            df = load_csv_safely(uploaded_file)
            st.success(f"✅ 已加载: {len(df)} 行 x {len(df.columns)} 列")

            # 用文件名+大小作为唯一标识（修复 AttributeError）
            file_key = f"{uploaded_file.name}_{uploaded_file.size}"

            # 如果是新文件，初始化 Agent
            if ('agent' not in st.session_state or
                    st.session_state.get('file_key') != file_key):
                st.session_state.agent = CSVAnalysisAgent(api_key=api_key)
                st.session_state.agent.load_data(df)
                st.session_state.file_key = file_key
                st.session_state.df = df

        except Exception as e:
            st.error(f"❌ 加载文件失败: {e}")

# 主界面
if 'agent' in st.session_state:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🔍 数据快照")
        st.dataframe(st.session_state.df.head(10))
        st.caption(f"总行数: {len(st.session_state.df)}")

    with col2:
        st.subheader("💬 分析指令")
        user_q = st.chat_input("例如: '计算各分类的销售总和' 或 '画一张箱线图'")

        if user_q:
            with st.spinner("🧠 Agent 正在生成代码并计算..."):
                res = st.session_state.agent.ask(user_q)

            st.chat_message("user").write(user_q)
            with st.chat_message("assistant"):
                if isinstance(res, plotly.graph_objects.Figure):
                    st.plotly_chart(res, use_container_width=True)
                elif isinstance(res, pd.DataFrame):
                    st.dataframe(res)
                else:
                    st.write(res)
else:
    st.info("👈 左侧上传文件并填写 Key 开始探索")