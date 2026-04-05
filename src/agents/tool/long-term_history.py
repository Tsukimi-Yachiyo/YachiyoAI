from langchain_core.messages import trim_messages
from langchain_core.messages.utils import count_tokens_approximately


def pre_model_hook(state):
    trimmed_message = trim_messages(
        state.message,
        strategy = "last",
        token_counter = count_tokens_approximately,
        max_tokens = 384,
        start_on = "human",
        end_on = "human"
    )
    return {"llm_input_message": trimmed_message}

