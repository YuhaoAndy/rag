# 交互式对话 - 可以和 AI 连续聊天
# 先安装: pip install openai

from openai import OpenAI

client = OpenAI(
    api_key="sk-3a332d349ed2428aaf2d7fddd558a2f1",
    base_url="https://api.deepseek.com"
)

# 存储对话历史
messages = [
    {"role": "system", "content": "You are a helpful assistant"}
]

print("🤖 AI 助手已启动！")


while True:
    # 获取用户输入
    user_input = input("你: ")
    
    # 检查是否退出
    if user_input.lower() in ['退出', 'quit', 'exit', 'q']:
        print("\n👋 再见！")
        break
    
    # 添加用户消息到历史
    messages.append({"role": "user", "content": user_input})
    
    # 调用 API
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )
        
        # 获取 AI 回复
        ai_reply = response.choices[0].message.content
        print(f"\n🤖 AI: {ai_reply}")
        
        # 添加 AI 回复到历史（保持上下文）
        messages.append({"role": "assistant", "content": ai_reply})
        
    except Exception as e:
        print(f"\n❌ 出错了: {e}")