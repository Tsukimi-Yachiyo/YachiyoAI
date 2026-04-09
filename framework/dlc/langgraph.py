"""
    langgraph
    基于 langgraph 实现的 langchain 应用
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

logger = logging.getLogger(__name__)

class Main(BaseMain):
    def __init__(self):

        self.app = None

        # 定义状态
        class State(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]

        self.workflow = StateGraph(State)
        library.dependencies["langgraph_node"] = {}
        library.dependencies["langgraph_edge"] = {}
        library.resource["first_node"] = []
        library.resource["last_node"] = []

    def build(self):
        for name, func in library.dependencies["langgraph_node"].items():
            self.workflow.add_node(name, func)

        can_run = False
        # 定义第一个节点
        for first_node in library.resource["first_node"]:
            self.workflow.set_entry_point(first_node)
            can_run = True

        # 定义最后一个节点
        for last_node in library.resource["last_node"]:
            self.workflow.add_edge(last_node, END)

        for name, func in library.dependencies["langgraph_edge"].items():
            from_node, map = library.resource["langgraph_edge"][name]
            if map is None:
                self.workflow.add_edge(from_node, func)
            else:
                self.workflow.add_conditional_edges(from_node, func, map)

        if can_run:
            self.app = self.workflow.compile()

        # 定义获取 langgraph 图的函数
        def get_graph():
            try:
                from IPython.display import display, Image
                display(Image(self.app.get_graph(xray=True).draw_png()))
            except Exception as e:
                logger.error(f"获取 langgraph 图失败: {e}")

        library.resource["get_graph"] = get_graph

        library.resource["langgraph_app"] = self.app

def langgraph_node(name: str = None, first_last: bool = None):
    def decorator(func):
        nonlocal name
        if name is None:
            name = func.__name__
        library.dependencies["langgraph_node"][name] = func
        if first_last is not None:
            if first_last:
                library.resource["first_node"].append(name)
            else:
                library.resource["last_node"].append(name)
        return func
    return decorator

def langgraph_edge(from_node: str = None, map: dict = None ,name: str = None):
    def decorator(func):
        nonlocal name
        if name is None:
            name = func.__name__
        library.dependencies["langgraph_edge"][name] = func
        library.resource["langgraph_edge"][name] = [from_node, map]
        return func
    return decorator
