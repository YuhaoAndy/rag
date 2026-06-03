from langchain_community.document_loaders import CSVLoader  # ✅ 对

document_loader = CSVLoader("data/data.csv", encoding="utf-8")

""" # 加载所有文档
documents = document_loader.load()
print(documents)  """

#懒加载  遍历文档
documents = document_loader.lazy_load()
for document in documents:
    print(document) 


#两个输出文档区别：
# 1. 加载所有文档：一次加载所有文档，返回一个列表。
# 2. 懒加载：每次迭代返回一个文档，适合处理大量文档。