from langchain_community.document_loaders import JSONLoader


loader1 = JSONLoader("data.json", jq_schema=".[]", text_content=False)
#.[] 表示展开数组中的每个元素
documents1 = loader1.load()

#print(documents1)


loader2 = JSONLoader("data3.json", jq_schema=".", text_content=False)
#. 表示展开所有字段
documents2 = loader2.load()

#print(documents2)  


loader3 = JSONLoader("data4.json", jq_schema=".", text_content=True)
#. 表示展开所有字段
documents3 = loader3.load()

#print(documents3)  


loader4 = JSONLoader("data2.json", jq_schema=".", text_content=False)
loader5 = JSONLoader("data2.json", jq_schema=".hobby[]", text_content=True)
loader6 = JSONLoader("data2.json", jq_schema=".other.addr", text_content=True)
loader7 = JSONLoader("data2.json", jq_schema=".hobby[0]", text_content=True)
loader8 = JSONLoader("data2.json", jq_schema=".other", text_content=False)
loader9 = JSONLoader("data2.json", jq_schema=".hobby[0:2]", text_content=False)

#. 表示展开所有字段     
#.users[] 表示展开 users 数组中的每个元素
#.hobby[] 表示展开 hobby 数组中的每个元素
#.other.addr 表示展开 other.addr 字段中的每个元素
#.hobby[0] 表示展开 hobby 数组中的第一个元素
#.other 表示展开 other 字段中的每个元素



documents4 = loader4.load()
documents5 = loader5.load()
documents6 = loader6.load()
documents7 = loader7.load()
documents8 = loader8.load()
documents9 = loader9.load()

#print(documents4)
#print(documents5)
#print(documents6)
#print(documents7)
#print(documents8)
print(documents9)








