
def to_text_dict(x: str) -> dict:  #接收str类型输入，返回dict类型输出
    """
    将字符串输出转换为 prompt2 需要的字典格式
    键名 "text" 对应 prompt2 中的 {text} 变量
    """
    return {"text": x}