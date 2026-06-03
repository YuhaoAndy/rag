# 带记忆的对话机器人
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# 创建模型
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-3a332d349ed2428aaf2d7fddd558a2f1",
    base_url="https://api.deepseek.com"
)

# 创建模板（包含历史消息占位符）
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的助手，记住我们的对话"),
    MessagesPlaceholder(variable_name="history"),  # 历史消息放这里
    ("human", "{input}")
])

# 存储历史消息
history = [] # 初始化空消息列表

# 对话循环
print("🤖 AI 助手（输入 '退出' 结束）")
print("-" * 40)

while True:
    user_input = input("\n👤 你: ")
    
    if user_input.lower() in ['退出', 'quit', 'q']:
        print("👋 再见！")
        break
    
    # 调用模型
    chain = prompt | llm
    result = chain.invoke({
        "history": history,
        "input": user_input
    })
    
    # 打印回复
    print(f"\n🤖 AI: {result.content}")
    
    # 保存到历史
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=result.content))