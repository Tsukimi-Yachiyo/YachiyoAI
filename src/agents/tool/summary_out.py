from persistent import yml
from llm import model

logger = logging.getLogger(__name__)

def summary_out(state: State):
    """
        摘要
    """
    system = SystemMessage(content=yml.all_yaml.get("summary_out_prompt"))
    user = HumanMessage(content=state.answer.content)
    if len(state.answer.content) > 100:
        logger.info(f"输入过长，开始压缩{state.answer.content}")
        state.answer = model.model_service.compress_model.invoke([system,user]).content
    else:
        logger.info(f"输入过短，直接返回{state.answer.content}")
        state.answer = state.answer.content
