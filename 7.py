# 提示词模板示例
# pip install langchain langchain-openai

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate # 导入 ChatPromptTemplate 类

# 创建模型
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-3a332d349ed2428aaf2d7fddd558a2f1",
    base_url="https://api.deepseek.com"
)

# 创建模板
template = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的{领域}翻译助手"),
    ("human", "请把以下内容翻译成{目标语言}: {内容}")
])

# 填充模板
prompt = template.invoke({ # invoke 方法填充模板
    "领域": "技术",
    "目标语言": "英文",
    "内容": "人工智能正在改变世界"
})


# 调用模型，非流式输出
response = llm.invoke(prompt)
print(f"AI回复: {response.content}")