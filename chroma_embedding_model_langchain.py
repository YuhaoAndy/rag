
import os, json
from typing import Sequence
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
    
import chromadb
from chromadb.utils import embedding_functions
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
# 导入提示模板和消息占位符
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder 
# 导入消息转换函数和基础消息类
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage 
# 导入聊天历史记录类
from langchain_core.chat_history import BaseChatMessageHistory
# 导入可运行对象和消息历史记录可运行对象
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction( # 创建嵌入函数
    model_name="BAAI/bge-small-zh-v1.5"  # 使用 BGE 嵌入模型（中文效果好）
)

# 创建本地客户端，启用持久化
chroma_client = chromadb.PersistentClient(path="./chroma_data_bge")


#创建集合时绑定嵌入模型，如果集合已存在则直接获取
collection = chroma_client.get_or_create_collection( 
    "my_collection_rag",
    embedding_function=embedding_fn   # 绑定 BGE 嵌入模型
)

if collection.count() == 0: #如果集合为空，添加样本
    collection.add(
        documents=[
            "猫喜欢吃鱼，它们是非常可爱的宠物，也喜欢吃猫粮和罐头",
            "狗是人类最忠诚的朋友，喜欢啃骨头和玩球",
            "Python是一种流行的编程语言，由Guido van Rossum于1991年创建",
            "今天天气很好，适合出去散步，阳光明媚"
        ],
        ids=["id1", "id2", "id3", "id4"]
    )



# 自定义聊天历史记录类，继承BaseChatMessageHistory类
class FileChatMessageHistory(BaseChatMessageHistory):  

# 初始化方法 传入会话ID和存储路径，创建会话文件夹并初始化空文件
    def __init__(self, session_id, storage_path): 
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(self.storage_path, self.session_id) # 会话文件路径
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
         # 创建会话文件夹 ，如果已存在则不创建

# 添加消息方法 传入消息序列，将消息转换为字典并写入文件
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)
        new_messages = [message_to_dict(message) for message in all_messages]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f, ensure_ascii=False)

    @property # 消息属性方法 从文件中读取消息并返回
    # 如果文件不存在，返回空列表
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None: # 清空方法 清空会话文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


def get_history(session_id): # 获取聊天历史记录方法
    return FileChatMessageHistory(session_id, "./rag_chat_history")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-3a332d349ed2428aaf2d7fddd558a2f1",
    base_url="https://api.deepseek.com"
)

# 检索方法 传入用户问题，返回集合中相似度最高的两个文档
# 如果集合为空，返回空字符串
def retrieve(input_dict):
    question = input_dict["question"]
    results = collection.query(query_texts=[question], n_results=2)
    return "\n".join(results['documents'][0])

template = ChatPromptTemplate.from_messages([
    ("system", "你是一个有帮助的助手。请根据以下参考资料回答用户的问题。如果参考资料中没有相关信息，请根据你的知识回答。\n\n参考资料：\n{context}"),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}")
])

base_chain = (
    RunnablePassthrough.assign(context=retrieve)  # 检索方法 传入用户问题，返回集合中相似度最高的两个文档
    | template
    | llm
    | StrOutputParser()
)

rag_chain = RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key="question",
    history_messages_key="chat_history"
)

if __name__ == "__main__":
    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }

    print("🤖 RAG AI 助手已启动！（输入 '退出' 结束对话）")
    print("-" * 40)

    while True:
        user_input = input("\n👤 你: ")

        if user_input.lower() in ['退出', 'quit', 'exit', 'q']:
            print("\n👋 再见！")
            break

        result = rag_chain.invoke(
            {"question": user_input},
            config=session_config
        )
        print(f"\n🤖 AI: {result}")
