from openai import OpenAI 

#使用openai api库调用deepseek模型的api

client = OpenAI(
    api_key="sk-3a332d349ed2428aaf2d7fddd558a2f1",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},  # 系统提示
        {"role": "user", "content": "你是谁"},   # 用户发送消息
    ],
    stream=False  # 非流式输出
    #stream=True  # 流式输出
)

# 非流式输出
print(response.choices[0].message.content)

# 流式输出
'''
for chunk in response:
    print(chunk.choices[0].delta.content, end="")
print() 
'''
 
