import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import messages_from_dict, message_to_dict, HumanMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-3a332d349ed2428aaf2d7fddd558a2f1",
    base_url="https://api.deepseek.com"
)

# 使用 MessagesPlaceholder 插入历史
template = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的助手，记住我们的对话"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

chain = template | llm | StrOutputParser()


# ========== JSON 文件存储 ==========

def load_history(session_id: str) -> InMemoryChatMessageHistory:
    """从 JSON 文件加载历史"""
    file_path = f"history_{session_id}.json"
    history = InMemoryChatMessageHistory()
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            messages = messages_from_dict(data)
            history.messages = messages
    
    return history


def save_history(session_id: str, history: InMemoryChatMessageHistory):
    """保存历史到 JSON 文件"""
    file_path = f"history_{session_id}.json"
    data = [message_to_dict(msg) for msg in history.messages]
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ========== 交互循环 ==========

if __name__ == "__main__":
    session_id = "user_001"
    
    # 加载历史
    history = load_history(session_id)
    
    print("🤖 AI 助手已启动！（输入 '退出' 结束对话）")
    print("-" * 40)
    
    while True:
        user_input = input("\n👤 你: ")
        
        if user_input.lower() in ['退出', 'quit', 'exit', 'q']:
            print("\n👋 再见！")
            break
        
        # 调用链（手动传入历史）
        result = chain.invoke({
            "history": history.messages,
            "question": user_input
        })
        
        print(f"\n🤖 AI: {result}")
        
        # 添加到历史
        history.add_message(HumanMessage(content=user_input))
        history.add_message(AIMessage(content=result))
        
        # 保存到文件
        save_history(session_id, history)
        print("💾 已保存")