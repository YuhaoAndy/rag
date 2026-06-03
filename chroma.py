import chromadb #一个开源的向量数据库，用于存储和检索向量数据
 
# 创建本地客户端，启用持久化
client = chromadb.PersistentClient(path="./chroma_data")  # 数据将保存到 ./chroma_data 目录

# 创建集合（如果已存在则获取）
collection = client.get_or_create_collection("my_collection")
#等价于数据库的表

collection.add(
    documents=["This is a document", "Another document"],  # 要添加的文档内容
    embeddings=[[1.2, 2.3, 4.5], [6.7, 8.2, 9.2]],  #每个文档对应的嵌入向量
    #在这里，第一个向量对应文档"This is a document"，第二个向量对应文档"Another document"

    #每个文档都有一个唯一的id，用于标识该文档
    #如果未指定id，会自动生成一个id
    ids=["id1", "id2"]
)

results = collection.query(
    query_embeddings=[[1.3, 2.1, 4.4]],  # 查询向量  与文档的嵌入向量进行相似度计算

    #如何计算的：
    # 余弦相似度(A·B) / (||A|| × ||B||)     计算查询向量与每个文档的嵌入向量的余弦相似度
    # 余弦相似度的范围是[-1, 1]，1表示完全相似，-1表示完全不相似，0表示不相关
    # 在这里，查询向量和第一个文档的嵌入向量的余弦相似度计算：
    # (1.3 * 1.2 + 2.1 * 2.3 + 4.4 * 4.5) / (||1.3, 2.1, 4.4|| × ||1.2, 2.3, 4.5||)
    # = 0.9999999999999999

    # 在这里，查询向量和第二个文档的嵌入向量的余弦相似度计算：
    # (1.3 * 6.7 + 2.1 * 8.2 + 4.4 * 9.2) / (||1.3, 2.1, 4.4|| × ||6.7, 8.2, 9.2||)
    # = 0.9999999999999999
    
    n_results=2# 返回的相似度最高的2个文档
)
print(results)
