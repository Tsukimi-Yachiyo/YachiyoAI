from os import terminal_size

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from .state import State
from .tool.summary_out import summary_out
from .tool.review import review
from .tool.tool_judgment import tool_judgment
from .tool.major_out import major_out
from .tool.common_topic_out import common_topic_out
from .tool.is_major_topic import is_major_topic
from .tool.is_special_topic import is_special_topic
from .tool.is_special_day import is_special_day
from .tool.is_persona_out import is_persona_out
from .tool.complete_persona_out import complete_persona_out
from .tool.long_term_history import long_term_history
from .tool.special_topic_out import special_topic_out
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
        workflow.add_node("review",review)
        workflow.add_node("is_persona_out",is_persona_out)
        workflow.add_node("is_special_day",is_special_day)
        workflow.add_node("is_special_topic",is_special_topic)
        workflow.add_node("is_major_topic",is_major_topic)
        workflow.add_node("long_term_history",long_term_history)
        workflow.add_node("special_topic_out",special_topic_out)
        workflow.add_node("common_topic_out",common_topic_out)
        workflow.add_node("complete_persona_out",complete_persona_out)
        workflow.add_node("major_out",major_out)
        workflow.add_node("tool_judgment",tool_judgment)
        workflow.add_node("summary_out",summary_out)

        workflow.set_entry_point("review")

        # 添加条件边
        workflow.add_conditional_edges(
            "review",
            self.should_continue,
            {
                True: END,  # True → 结束流程
                False: "is_persona_out"  # False → 去下一个节点
            }
        )
        workflow.add_conditional_edges(
            "is_persona_out",
            self.is_output,
            {
                True: "complete_persona_out",
                False: "long_term_history"
            }
        )
        workflow.add_edge("long_term_history","is_special_day")
        workflow.add_edge("is_special_day","is_special_topic")
        workflow.add_conditional_edges(
            "is_special_topic",
            self.is_output,
            {
                True: "special_topic_out",
                False: "is_major_topic"
            }
        )
        workflow.add_conditional_edges(
            "is_major_topic",
            self.is_output,
            {
                True: "major_out",
                False: "common_topic_out"
            }
        )
        workflow.add_edge("tool_judgment","common_topic_out")

        workflow.add_edge("common_topic_out","summary_out")
        workflow.add_edge("major_out","summary_out")
        workflow.add_edge("special_topic_out","summary_out")
        workflow.add_edge("complete_persona_out","summary_out")

        workflow.add_edge("summary_out",END)

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

    @staticmethod
    def which_node(state):
        return state["judgment_node"]

    @staticmethod
    def is_output(state):
        return state["judgment"]
