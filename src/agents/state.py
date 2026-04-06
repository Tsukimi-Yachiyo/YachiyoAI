from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

# 状态定义
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    query: str
    config: dict

    need_reflect: bool
    judgment: bool
    judgment_node: str
    stop: bool
