import streamlit as st
import pandas as pd
from csv_agent import CSVAnalysisAgent, load_csv_safely  # 从包导入
import plotly
import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件

st.set_page_config(layout="wide")
st.title("📊 CSV 智能分析 Agent")

with st.sidebar:
    st.header("⚙️ 配置")
    # 优先从env取，未取到则让用户输入
    default_key = os.getenv("DeepSeek API Key", "")
    api_key = st.text_input("DeepSeek API Key", value=default_key, type="password", placeholder="sk-xxxxxxxx")
    uploaded_file = st.file_uploader("上传 CSV 文件", type=["csv"])

    if uploaded_file and api_key:
        df = load_csv_safely(uploaded_file)
        st.success(f"✅ 已加载: {len(df)} 行 x {len(df.columns)} 列")
        if 'agent' not in st.session_state or st.session_state.get('file_id') != uploaded_file.id:
            st.session_state.agent = CSVAnalysisAgent(api_key=api_key, model="deepseek-coder")
            st.session_state.agent.load_data(df)
            st.session_state.file_id = uploaded_file.id
            st.session_state.df = df

if 'agent' in st.session_state:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("🔍 数据快照")
        st.dataframe(st.session_state.df.head(10))
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
                else:
                    st.write(res)
else:
    st.info("👈 左侧上传文件并填写 Key 开始探索")