import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com" #为了顺利下载BAAI/bge-small-zh-v1.5模型

import chromadb
from chromadb.utils import embedding_functions # 导入嵌入函数
 

# 使用 BGE 嵌入模型（中文效果好）
# BAAI/bge-small-zh-v1.5 是北京智源研究院开发的中文嵌入模型
# 将文本转换为512维向量，首次运行会自动下载模型（约100MB）
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction( # 创建嵌入函数
    model_name="BAAI/bge-small-zh-v1.5"
)

# 创建本地客户端，启用持久化
client = chromadb.PersistentClient(path="./chroma_data_bge")

# 创建集合时绑定嵌入模型，如果集合已存在则直接获取
collection = client.get_or_create_collection(
    "my_collection_bge",
    embedding_function=embedding_fn  # 绑定 BGE 嵌入模型
)

collection.add(
    documents=[
        "猫喜欢吃鱼，它们是非常可爱的宠物",
        "狗是人类最忠诚的朋友，喜欢啃骨头",
        "Python是一种流行的编程语言",
        "今天天气很好，适合出去散步"
    ],
    ids=["id1", "id2", "id3", "id4"]  
)

# 查询时直接传入文本，模型自动将查询文本转换为向量
results = collection.query(
    query_texts=["小猫爱吃什么"],
    n_results=2  # 返回2个最相似的文档
) 
'''
#得到results为一个字典，包含documents、ids、distances三键
#   results{
#    "documents": ["猫喜欢吃鱼，它们是非常可爱的宠物", "狗是人类最忠诚的朋友，喜欢啃骨头"],
#    "ids": ["id1", "id2"],
#    "distances": [0.0, 0.0]
     }
'''

print("查询: 小猫爱吃什么")
print(f"最相似的文档: {results['documents'][0]}") #返回documents的第一个元素
print(f"最相似的文档id: {results['ids'][0]}")
print(f"相似度距离: {results['distances'][0]}")
print()

