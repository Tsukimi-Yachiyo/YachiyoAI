from langchain_openai import ChatOpenAI
from src.config import settings


class ModelDepository:

    def __init__(self):
        self.models = []
        self.compress_model = ChatOpenAI(
            model=settings.COMPRESS_MODEL_NAME,
            api_key=settings.DASHSCOPE_API_KEY,
            base_url=settings.BASE_URL,
            temperature=0.7
        )
        self.models.append(
            ChatOpenAI(
                model=settings.MODEL_NAME,
                api_key=settings.DASHSCOPE_API_KEY,
                base_url=settings.BASE_URL,
                temperature=0.7
            )
        )

    def add_model(self, llm_model : str,
                  api_key : str,
                  base_url : str,
                  temperature : float = 0.7):
        self.models.append(
            ChatOpenAI(
                model=llm_model,
                api_key=api_key,
                base_url=base_url,
                temperature=temperature
            )
        )

    def delete_model(self, name : str):
        if name is not None:
            for llm_model in self.models:
                if llm_model.name == name:
                    self.models.remove(llm_model)
        else:
            self.models.pop(0)

    def get_llm(self):
        return self.models[0]

model = ModelDepository()
