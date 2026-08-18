# 📊 CSV Analysis Agent

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?logo=openai)](https://openai.com/)

> 基于自然语言驱动的CSV数据分析助手，让不懂代码的人也能通过对话完成数据清洗、统计与可视化。

## ✨ 功能亮点
- 🗣️ **自然语言交互**：输入“按地区分组求和”即可生成分析结果。
- 📈 **智能可视化**：自动识别数据特征，生成交互式图表（Plotly）。
- 🔧 **动态代码生成**：利用大模型生成Pandas代码，灵活应对复杂分析需求。

## 🚀 快速开始
1. 克隆项目
```bash
git clone https://github.com/RuoyuZ/csv-analysis-agent.git
cd csv-analysis-agent
```


2. 安装依赖（推荐使用虚拟环境）

```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .          # 以可编辑模式安装包
```

3. 配置环境变量
````
cp .env.example .env
# 编辑 .env 文件，填入你的 OPENAI_API_KEY
````


4. 启动应用
````
streamlit run app.py
````