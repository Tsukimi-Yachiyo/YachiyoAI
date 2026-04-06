from openai import  RateLimitError, BadRequestError
from persistent import yml
from llm import model
from .postgre_vector import max_retrieve_documents

logger = logging.getLogger(__name__)
llm = model.model_service.get_llm().bind_tools([max_retrieve_documents])

async def complete_persona_out(state: State):
    """
        完善角色描述
    """
    prompt = yml.all_yaml.get("complete_personal_prompt")
    try:
        answer = await llm.ainvoke(prompt)
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
