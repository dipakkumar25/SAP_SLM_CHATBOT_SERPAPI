from setuptools import setup, find_packages

setup(
    name="sap-smart-chatbot",
    version="1.0.0",
    description="SAP Intelligent Support Assistant with RAG capabilities",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "faiss-cpu>=1.7.0",
        "sentence-transformers>=2.2.0",
        "requests>=2.28.0",
        "python-dotenv>=0.19.0",
        "openpyxl>=3.0.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)