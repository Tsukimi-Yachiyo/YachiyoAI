import json

from ..state import State
from persistent import json

def review(state: State):

    current_message = state["messages"]

    keyword = json.all_json["SENSITIVE_WORDS"]

    for key in keyword:
        if key in current_message:
            return {"stop": True}

    return {"stop": False}




