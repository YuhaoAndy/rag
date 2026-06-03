# RAG 基础实现

基于检索增强生成（Retrieval-Augmented Generation）的问答系统基础实现。

## 项目结构

```
├── data/                    # 数据文件（csv, json, pdf, txt）
├── loader/                  # 数据加载器
│   ├── csvloder.py
│   ├── jsonloder.py
│   ├── pdfloader.py
│   └── txtloader.py
├── utils/                   # 工具函数
│   ├── __init__.py
│   └── to_text_dict.py
├── chroma_data/             # ChromaDB 向量存储（默认 embedding）
├── chroma_data_bge/         # ChromaDB 向量存储（BGE embedding）
├── chat_history/            # 聊天历史记录
├── rag_chat_history/        # RAG 聊天历史记录
├── 1.openai-ez-chat.py      # OpenAI 简易聊天
├── 2.openai-chatbot.py      # OpenAI 聊天机器人
├── 5.py                     # RAG 基础流程
├── 7.py                     # RAG + 历史记录
├── 8.py                     # RAG 优化
├── 9.py                     # RAG + LangChain
├── 10.py                    # RAG 系统
├── 11.py                    # RAG 系统迭代
├── 12.py                    # RAG 系统迭代
├── 13.py                    # RAG 系统迭代
├── chroma.py                # ChromaDB 基础操作
├── chroma_embedding_model.py          # ChromaDB + embedding 模型
├── chroma_embedding_model_langchain.py # ChromaDB + LangChain
├── long_chain.py            # LangChain 长链
├── 向量存储.py               # 向量存储操作
└── requirements.txt         # 项目依赖
```

## 功能特性

- 支持多种文档格式加载（TXT、CSV、JSON、PDF）
- 基于 ChromaDB 的向量存储与检索
- 支持多种 Embedding 模型（默认 + BGE）
- 集成 OpenAI API 进行生成
- 支持对话历史记录管理
- 基于 LangChain 的链式调用

## 快速开始

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
创建 `.env` 文件，添加 OpenAI API Key：
```
OPENAI_API_KEY=your_api_key_here
```

3. 运行示例：
```bash
python 5.py
```

## 依赖

- Python 3.10+
- OpenAI API
- ChromaDB
- LangChain
