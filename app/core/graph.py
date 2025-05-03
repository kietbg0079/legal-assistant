from app.model import LLMModel
from .state import State
from langgraph.graph import StateGraph, START, END

def define_graph(llm):
    graph_builder = StateGraph(State)

    def chatbot(state: State):
        return {"messages": [llm.invoke(state["messages"])]}
    
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    graph = graph_builder.compile()

    return graph

llm = LLMModel()()
graph = define_graph(llm)

def chat_handle(message: str):    
    for event in graph.stream({"messages": [{"role": "user", "content": message}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
    return 