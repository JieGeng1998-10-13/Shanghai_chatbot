from langgraph.graph import StateGraph
from router_selection import Router  # 导入自定义的选择路由类
from retriever_SQL import SQLModelHandler  # 导入自定义的SQL类
from utils.tools import GraphState  # 图结构数据类型声明
from langgraph.graph import MessagesState, END
from utils.function_tools import route_question, call_model, call_model_SQL, call_model_SQL_prompt, route_question2

router_instance = Router()
instructions = router_instance.router_instructions
llm = router_instance.llm
retriever1 = SQLModelHandler()




workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("answer_directly", call_model)  # web search
workflow.add_node("retrieve_SQL_prompt", call_model_SQL_prompt)
workflow.add_node("retrieve_SQL", call_model_SQL)  # retrieve
# workflow.add_node("retrieve_law", call_model_retrieve_law)
workflow.add_edge("answer_directly", END)
workflow.add_edge("retrieve_SQL_prompt", "retrieve_SQL")
#workflow.add_edge("retrieve_SQL", END)

# Build graph
workflow.set_conditional_entry_point(
    route_question,
    {
        "answer_directly": "answer_directly",
        "vectorstore": "retrieve_SQL_prompt",
    },
)


workflow.add_conditional_edges(
    "retrieve_SQL",
    route_question2,
    {
        "correct": END,
        "wrong": "retrieve_SQL_prompt"
    }
)


graph = workflow.compile()

inputs = {"question": "中标结果一共有多少条"}
for event in graph.stream(inputs, stream_mode="values"):
    print(event)
