from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils import to_text_dict

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-3a332d349ed2428aaf2d7fddd558a2f1",
    base_url="https://api.deepseek.com"
)

# 第一步：生成回答
prompt1 = ChatPromptTemplate.from_messages([
    ("system", "你是一个{风格}的助手"),
    ("human", "{问题}")
])

# 第二步：翻译或进一步处理
prompt2 = ChatPromptTemplate.from_messages([
    ("system", "你是一个文言文专家，将以下内容翻译成文言文"),
    ("human", "{text}")
])


# 构建长链
chain = (  
    prompt1 
    | llm 
    | StrOutputParser()  # 解析模型输出为字符串
    | to_text_dict  # 转换格式，将字符串包装成字典格式，以便传递给下一个 prompt
    | prompt2 
    | llm 
    | StrOutputParser()
)

result = chain.invoke({
    "风格": "幽默",
    "问题": "什么是人工智能？"
})

print(result)