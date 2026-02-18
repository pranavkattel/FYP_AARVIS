from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage,ToolMessage, SystemMessage, AIMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph,START,END
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import ToolNode


document_content = ""

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]
    
@tool
def update(content:str) -> str:
    """this is an update function that updates the document content."""
    global document_content
    document_content = content
    return "Document updated successfully."