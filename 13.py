import os, json #文件操作、json字符串
from typing import Sequence 
 
from langchain_openai import ChatOpenAI
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
#把单个消息对象转换为字典   把多个字典转换为消息对象  消息基类，所有其他消息类的父类
from langchain_core.chat_history import BaseChatMessageHistory #聊天历史基类
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory#可运行的链，带消息历史
 
 
# message_to_dict：单个消息对象（BaseMessage类实例） -> 字典
# messages_from_dict：[字典、字典...]  -> [消息、消息...]
# AIMessage、HumanMessage、SystemMessage 都是BaseMessage的子类
 

 #langchain规定的BaseChatMessageHistory自带哪些方法，如：add_messages、clear、messages等
 # 这些方法都是为了方便操作聊天历史记录而提供的的，我们可以在自定义类中调用这些方法
 # 可以直接调用add_messages方法添加消息，这不是自定义的方法，而是BaseChatMessageHistory类的方法，是继承过来的，那为什么可以直接调用吗？
 # 因为在自定义类中，我们已经将BaseChatMessageHistory类的方法添加到了self对象中，所以可以直接调用。
 
class FileChatMessageHistory(BaseChatMessageHistory): # 自定义聊天历史类  继承聊天历史基类
    def __init__(self, session_id, storage_path):  # 初始化方法 创建这个类的对象时自动运行
        #self: 当前对象实例   self.属性名 = 值  给当前对象添加属性  会话id、存储路径、完整路径
        self.session_id = session_id        # 会话id
        self.storage_path = storage_path    # 不同会话id的存储文件，所在的文件夹路径
        # 完整的文件路径
        self.file_path = os.path.join(self.storage_path, self.session_id)
        #拼接两个路径  storage_path + session_id = 完整路径
        #./chat_history/user_001
 
        # 确保文件夹是存在的
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
       ##os.path.dirname()：返回文件路径的目录部分   是./chat_history
       #os.makedirs()：创建这个目录  exist_ok=True：而且如果目录已存在，不会报错
       
    
 
    def add_messages(self, messages: Sequence[BaseMessage]) -> None: 
        # Sequence序列 类似list、tuple
        all_messages = list(self.messages)      # 已有的消息列表
        all_messages.extend(messages)           # 新的和已有的融合成一个list
 
        # 将数据同步写入到本地文件中
        # 类对象写入文件 -> 一堆二进制
        # 为了方便，可以将BaseMessage消息转为字典（借助json模块以json字符串写入文件）
        # 官方message_to_dict：单个消息对象（BaseMessage类实例） -> 字典
        # new_messages = []
        # for message in all_messages:
        #     d = message_to_dict(message)
        #     new_messages.append(d)
 
        new_messages = [message_to_dict(message) for message in all_messages]
        # 将数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)
 
    @property       # @property装饰器将messages方法变成成员属性用
    def messages(self) -> list[BaseMessage]:
        # 当前文件内： list[字典]
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)    # 返回值就是：list[字典]
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []
 
    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)
 
 
 
 
 
model = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-3a332d349ed2428aaf2d7fddd558a2f1",
    base_url="https://api.deepseek.com"
)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据会话历史回应用户问题。对话历史："),
        MessagesPlaceholder("chat_history"), #专门用于占位历史消息的占位符
        ("human", "请回答如下问题：{input}")
    ]
)
 
str_parser = StrOutputParser()
 
 
def print_prompt(full_prompt):
    print("="*20, full_prompt.to_string(), "="*20)  
    # 打印full_prompt对象的字符串表示  是一个json字符串
    return full_prompt
 
 
base_chain = prompt | print_prompt | model | str_parser
'''LangChain 的 | 管道会自动传： 上一步的 输出 ，变成下一步的 输入

prompt的输出为一个PromptTemplate对象   给print_prompt函数作为输入
包含：
- 系统消息 SystemMessage
- 历史消息 AIMessage
- 用户输入消息 HumanMessage


再传给model模型  得到模型的输出  再传给str_parser解析器  得到最终的字符串输出

'''


 
def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history") 
    #把session_id和./chat_history这个文件夹路径作为参数  返回一个FileChatMessageHistory类对象
 
# 创建一个新的链，对原有链增强功能：自动附加历史消息
conversation_chain = RunnableWithMessageHistory(
    base_chain,     # 被增强的原有chain
    get_history,    # 通过会话id获取InMemoryChatMessageHistory类对象
    input_messages_key="input",             #input_messages_key 表示用户输入在模板中的占位符
    history_messages_key="chat_history"     # history_messages_key 表示历史消息在模板中的占位符
   
)
 
 
if __name__ == '__main__':
    # 固定格式，添加LangChain的配置，为当前程序配置所属的session_id
    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }
 
    res = conversation_chain.invoke({"input": "小明有2个猫"}, session_config)
    print("第1次执行：", res)
    
    res = conversation_chain.invoke({"input": "小刚有1只狗"}, session_config)
    print("第2次执行：", res)
 
    res = conversation_chain.invoke({"input": "总共有几个宠物"}, session_config)
    print("第3次执行：", res)