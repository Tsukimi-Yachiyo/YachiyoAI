from langchain_core.messages import SystemMessage, ToolMessage
from openai import  RateLimitError, BadRequestError
from persistent import yml
from llm import model
from .postgre_vector import max_retrieve_documents

logger = logging.getLogger(__name__)
llm = model.model_service.get_llm()

async def complete_persona_out(state: State):
    """
        完善角色描述
    """
    docs = await max_retrieve_documents(state["query"])
    docs_content = ""
    for i, doc in enumerate(docs):
        docs_content = f"{docs_content}{i+1}.{doc.page_content}\n"

    prompt = """{
    "system":
        [%s ],
    "docs":
        [%s ],
    "your_task":
        "根据请按照人设和设定补充，回答用户的问题。"
        }
    """%(yml.all_yaml.get("complete_personal_prompt"),docs_content)
    system = SystemMessage(content=prompt)
    user = HumanMessage(content=state["query"])
    logger.info(f"输入{state['query']}")
    logger.info(f"文档{docs_content}")
    try:
        answer = await llm.ainvoke([system,user])
        logger.info(f"模型回复{answer.content}")
        if answer.content:
            state.answer = answer.content
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
