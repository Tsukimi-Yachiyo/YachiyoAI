from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage

# 状态定义
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "add"]
    need_reflect: bool