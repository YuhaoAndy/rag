from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-3a332d349ed2428aaf2d7fddd558a2f1",
    base_url="https://api.deepseek.com"
)

template = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的助手，记住我们的对话\n\n历史记录：{history}"),
    ("human", "{question}")
])

chain = template | llm | StrOutputParser()

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

# ========== 下面添加交互循环 ==========
if __name__ == "__main__":
    session_id = "user_001"  # 当前用户ID
    
    print("🤖 AI 助手已启动！（输入 '退出' 结束对话）")
    print("-" * 40)
    
    while True:
        # 获取用户输入
        user_input = input("\n👤 你: ")
        
        # 检查是否退出
        if user_input.lower() in ['退出', 'quit', 'exit', 'q']:
            print("\n👋 再见！")
            break
        
        # 调用带历史的链
        result = chain_with_history.invoke(
            {"question": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        
        # 打印AI回复
        print(f"\n🤖 AI: {result}")