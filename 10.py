from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory# 增加了历史记录的链
from langchain_core.chat_history import InMemoryChatMessageHistory
# 历史记录存储

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-3a332d349ed2428aaf2d7fddd558a2f1",
    base_url="https://api.deepseek.com"
)

# 模板：history 会被自动格式化为字符串
template = ChatPromptTemplate.from_messages([
    ("system", "你需要根据会话历史记录，回答用户的问题\n会话历史记录: {history}"),
    ("human", "{question}")
])

chain = template | llm | StrOutputParser()

# 用于存储所有会话的历史记录（内存中）
store = {}

#session_id 会话id 用于标识每个会话
def get_session_history(session_id: str):

    if session_id not in store: # 如果会话id不存在
        # 创建一个新的历史记录
        # 每个会话都有一个历史记录，用于存储用户的问题和助手的回答
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 将普通链包装成带历史记录的链
chain_with_history = RunnableWithMessageHistory(
    chain,                           # 你的基础链
    get_session_history,             # 获取历史的函数
    input_messages_key="question",   # 用户新问题的键名
    history_messages_key="history"   # 历史记录的键名
)

# 测试第一轮
result1 = chain_with_history.invoke(
    {"question": "你好，我叫小明"},
    config={"configurable": {"session_id": "user_001"}}
)
print(f"第一轮: {result1}")

print("-" * 40)

# 测试第二轮（AI应该记得名字）
result2 = chain_with_history.invoke(
    {"question": "我叫什么名字？"},
    config={"configurable": {"session_id": "user_001"}}
)
print(f"第二轮: {result2}")
print("-" * 40)

# 测试第三轮）
result3 = chain_with_history.invoke(
    {"question": "我前面问了你什么问题"},
    config={"configurable": {"session_id": "user_001"}}
)
print(f"第三轮: {result3}")