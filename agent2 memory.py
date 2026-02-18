from typing import TypedDict, List, Union
import re
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph,START,END

llm = ChatOllama(model="llama3.2:1b", temperature=0.9)

class AgentState(TypedDict):
    messages : List[Union[HumanMessage, AIMessage]]


def process(state: AgentState) -> AgentState:
    """this node will solve the request of the input"""
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))
    print(f"AI: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

conversation_history = []

user_input = input("Enter your message: ")
while user_input.lower() != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({
        "messages": conversation_history
    })
    print(f"AI: {result['messages'][-1].content}")
    conversation_history = result["messages"]
    user_input = input("Enter your message: ")

with open("conversation_history.txt", "w") as f:
    f.write("Conversation History:\n")
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            f.write(f"Human: {message.content}\n")
        else:
            f.write(f"AI: {message.content}\n")
    f.write("End of Conversation\n")

print("Conversation history saved to conversation_history.txt")