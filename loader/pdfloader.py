from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/data.pdf")   

documents = loader.load() #加载PDF文件
print(documents) 

     