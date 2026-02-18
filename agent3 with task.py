from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage,ToolMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph,START,END
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import ToolNode

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]    


@tool 
def add(a: int, b: int) -> int:
    """this ia an addition funtion that Add two numbers together."""
    return a + b   

def subtract(a: int, b: int) -> int:
    """this is a subtraction function that subtracts two numbers."""
    return a - b

def multiply(a: int, b: int) -> int:
    """this is a multiplication function that multiplies two numbers."""
    return a * b

tools = [add, subtract, multiply]

model = ChatOllama(model="llama3.2:1b").bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are a helpful assistant. Please answer my query to the best of your ability")
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}    

def should_continue(state: AgentState):
    message = state["messages"]
    last_message = message[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"    

graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)
tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")
graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)

graph.add_edge("tools", "our_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

input = {"messages": [("user", "add 3+4. subtract 2 and 5 and multiply the result by 9. Also tell me a joke by combining all the answers together")]}
print_stream(app.stream(input,stream_mode="values"))