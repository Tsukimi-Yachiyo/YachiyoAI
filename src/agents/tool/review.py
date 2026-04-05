import json

from ..state import State
from persistent import json

def review(state: State):
    """
        审核当前消息是否包含敏感词
    """
    current_message = state["messages"]

    keyword = json.all_json["SENSITIVE_WORDS"]

    for key in keyword:
        if key in current_message:
            return {"stop": True}

    return {"stop": False}




