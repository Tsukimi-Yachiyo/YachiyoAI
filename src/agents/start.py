from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from agents.tool.review import review
from .state import State
from .tool.summary_out import summary_out
from langgraph.graph import END
from .other.display import start_agent

class StartAgent:

    def __init__(self, chatLLM: ChatOpenAI):
        self.chatLLM = chatLLM

        workflow = StateGraph(State)

        workflow.add_node("summary_out",summary_out)
        workflow.add_node("review",review)


        workflow.set_entry_point("review")

        workflow.add_conditional_edges(
            "review",
            self.should_continue
        )

        self.app = workflow.compile()

    def get_graph(self):
        start_agent(self.app)

    def get_state(self):
        return self.app

    @staticmethod
    def should_continue(state):
        if state["stop"]:
            return True
        return False
