from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 创建模型
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-3a332d349ed2428aaf2d7fddd558a2f1",
    base_url="https://api.deepseek.com"
)

# 创建模板
prompt = ChatPromptTemplate.from_messages([  
    ("system", "你是一个{风格}的助手"),
    ("human", "{问题}")
])

# 加长链：模板 + 模型 + 输出解析器
chain = prompt | llm | StrOutputParser()

# 调用链
result = chain.invoke({
    "风格": "幽默",
    "问题": "什么是人工智能？"
})

print(result)  # 有解析器就可以直接输出字符串，否则需要result.content