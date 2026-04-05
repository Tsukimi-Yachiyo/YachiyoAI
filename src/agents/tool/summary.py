"""
    主体
"""
from ..state import State
from ..other.prompt import prompt_dict
from langchain_openai import ChatOpenAI

def summary(state: State,llm: ChatOpenAI):
    """
        摘要
    """

    prompt = prompt_dict["summary"]
    state.answer = llm.invoke(prompt)
