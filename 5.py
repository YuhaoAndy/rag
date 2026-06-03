# 简单的 LangChain 示例
# 先安装: pip install langchain langchain-openai

from langchain_openai import ChatOpenAI 
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage 


# 创建模型（使用本地 Ollama 的 Qwen3-8B 模型）
llm = ChatOpenAI(
    model="modelscope.cn/Qwen/Qwen3-8B-GGUF:latest",
    api_key="ollama",                    # 本地 Ollama 模型
    base_url="http://localhost:11434/v1",  # 本地 Ollama 模型的 URL
    temperature=0.7    
)

# 定义消息
messages = [
    SystemMessage(content="你是一个诗人"),
    HumanMessage(content="写一首唐诗"),
    AIMessage(content="锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),
    HumanMessage(content="按上面的格式写一首唐诗")
]

'''
# 调用模型
response = llm.invoke(messages)
# 打印回复
print(f"\nAI: {response.content}")
'''

#流式

for chunk in llm.stream(messages):
    print(chunk.content, end="")
print() 