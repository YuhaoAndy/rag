from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter # 文本分割器

loader = TextLoader("data/data.txt", encoding="utf-8")

documents=  loader.load() #加载文本文件
#print(documents) 


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,    # 每块100个字符
    chunk_overlap=20   # 块之间重叠20个字符
)

documents2 = text_splitter.split_documents(documents)
for doc in documents2:
    print(doc) #
    print("\n")
   
