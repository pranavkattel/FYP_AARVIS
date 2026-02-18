from typing import TypedDict, List
import re
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph,START,END


class AgentState(TypedDict):
    messages : List[HumanMessage]

llm = ChatOllama(model="qwen3:4b", temperature=0.9)

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state['messages'])
    text = response.content
    text = re.sub(r"(?s)<think>.*?</think>\s*", "", text).strip()
    print("LLM Response:", text)
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

user_input = input("Enter your message: ")
agent.invoke({
    "messages": [HumanMessage(content=user_input)]
})