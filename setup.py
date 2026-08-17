from setuptools import setup, find_packages

setup(
    name="csv-analysis-agent",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "streamlit",
        "pandas",
        "plotly",
        "openai",
        "python-dotenv"
    ],
    author="RuoyuZ",
    description="A conversational AI agent for CSV data analysis",
    python_requires=">=3.8",
)