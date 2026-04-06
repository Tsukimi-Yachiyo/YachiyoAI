from persistent import yml
from llm import model

def summary_out(state: State):
    """
        摘要
    """
    prompt = yml.all_yaml.get("summary_out_prompt")
    state.answer = model.model_service.compress_model.invoke(prompt)
