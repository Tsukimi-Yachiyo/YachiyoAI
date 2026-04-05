from openai import  RateLimitError, BadRequestError
from ..state import State
from persistent import yml
from llm import model
from tool import logging

logger = logging.getLogger(__name__)

def summary_out(state: State):
    """
        完善角色描述
    """
    prompt = yml.all_yaml.get("complete_personal_prompt")
    try:
        answer = model.model_service.get_llm().invoke(prompt)
        if answer:
            state.answer = answer
            return {"repeat":False}
        else:
            return {"repeat":True}
    except RateLimitError:
        model.model_service.delete_model()
        return {"repeat":True}
    except BadRequestError as e:
        logger.error(e)
        if "context_length_exceeded" in str(e).lower():
            return {"repeat":False,"summary": True }
        else:
            return {"repeat":True}
