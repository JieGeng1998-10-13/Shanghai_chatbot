from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore
from langchain_ollama import ChatOllama
from langgraph.graph import MessagesState

llm = ChatOllama(
    model="EntropyYue/chatglm3:6b",
)
class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)

def call_model(state: MessagesState):
    """
    调用模型生成响应。

    Args:
        state (MessagesState): 消息状态

    Returns:
        dict: 包含响应消息的字典
    """
    messages = state['question']
    vn = MyVanna(config={'model': 'EntropyYue/chatglm3:6b'})

    vn.connect_to_sqlite('上海市交通系统交易情况.db')

    result = vn.generate_sql(question=messages)
    f_result = vn.run_sql(result)

    response = llm.invoke(f_result)
    return {"generation": [response]}

vn = MyVanna(config={'model': 'EntropyYue/chatglm3:6b'})

vn.connect_to_sqlite('上海市交通系统交易情况.db')

# result = vn.generate_sql(question="一共有多少公司中过标？")
# try:
#     f_result = vn.run_sql(result)
# except Exception as e:
#     f_result= "查询失败"
#
# print("-------------------------------------------------------------")
# print(f_result)
from vanna.flask import VannaFlaskApp
VannaFlaskApp(vn).run()