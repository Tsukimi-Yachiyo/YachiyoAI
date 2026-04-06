from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from src.config import settings
from persistent import yml
import logging

model_service = None

logger = logging.getLogger(__name__)

class ModelDepository:

    def __init__(self):
        self.models = []
        self.compress_model = ChatOpenAI(
            model=settings.COMPRESS_MODEL_NAME,
            api_key=yml.all_yaml.get("llm.api_key"),
            base_url=settings.BASE_URL,
            temperature=0.7
        )
        self.embeddings_model = OpenAIEmbeddings(
            model=settings.EMBEDDINGS_MODEL_NAME,
            api_key=yml.all_yaml.get("llm.api_key"),
            base_url=settings.BASE_URL
        )
        self.models.append(
            ChatOpenAI(
                model=settings.MODEL_NAME,
                api_key=yml.all_yaml.get("llm.api_key"),
                base_url=settings.BASE_URL,
                temperature=0.7
            )
        )

    def add_model(self, llm_model : str,
                  api_key : str,
                  base_url : str,
                  temperature : float = 0.7):
        try:
            self.models.append(
                ChatOpenAI(
                    model=llm_model,
                    api_key=api_key,
                    base_url=base_url,
                    temperature=temperature
                )
            )
            logger.info(f"Add model {llm_model}")
        except Exception as e:
            logger.error(f"Add model {llm_model} failed: {e}")

    def delete_model(self, name : str):
        if name is not None:
            for llm_model in self.models:
                if llm_model.name == name:
                    self.models.remove(llm_model)
                    logger.info(f"Delete model {name}")
        else:
            self.models.pop(0)
            logger.info(f"Delete model {self.models[0].name}")

    def get_llm(self):
        return self.models[0]

def model_init():
    global model_service
    model_service = ModelDepository()
    logger.info("模型服务初始化")
