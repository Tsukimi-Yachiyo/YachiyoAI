from openai import  RateLimitError, BadRequestError
from ..state import State
from persistent.yml import all_yaml
from llm.model import model
from tool import logging

logger = logging.getLogger(__name__)

def summary_out(state: State):
    """
        完善角色描述
    """
    prompt = all_yaml.get("complete_personal_prompt")
    try:
        answer = model.get_llm().invoke(prompt)
        if answer:
            state.answer = answer
            return {"return":False}
        else:
            return {"return":True}
    except RateLimitError:
        model.delete_model()
    except BadRequestError as e:
        logger.error(e)
        if "context_length_exceeded" in str(e).lower():
            return {"return":False,"summary": True }
        else:
            return {"return":True}
