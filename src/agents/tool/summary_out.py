from ..state import State
from persistent.yml import all_yaml
from llm.model import model

def summary_out(state: State):
    """
        摘要
    """
    prompt = all_yaml.get("summary_out_prompt")
    state.answer = model.compress_model.invoke(prompt)
