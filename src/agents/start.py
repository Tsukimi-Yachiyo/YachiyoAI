from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from agents.tool.review import review
from .state import State
from .tool.summary_out import summary_out
from langgraph.graph import END
from .other.display import start_agent

# 启动智能体
class StartAgent:


    """
        启动智能体
        :param chatLLM: 语言模型
        :return: 智能体实例
    """
    def __init__(self, chatLLM: ChatOpenAI):
        self.chatLLM = chatLLM

        # 定义状态图
        workflow = StateGraph(State)

        # 添加节点
        workflow.add_node("summary_out",summary_out)
        workflow.add_node("review",review)

        # 设置入口点
        workflow.set_entry_point("review")

        # 添加条件边
        workflow.add_conditional_edges(
            "review",
            self.should_continue
        )

        # 编译状态图
        self.app = workflow.compile()

    """
        绘制状态图
    """
    def get_graph(self):
        start_agent(self.app)

    """
        获取当前状态图实例
        :return: 状态图实例
    """
    def get_state(self):
        return self.app

    """
        判断是否继续执行
        :param state: 状态
        :return: 是否继续执行
    """
    @staticmethod
    def should_continue(state):
        if state["stop"]:
            return True
        return False

