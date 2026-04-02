import uvicorn
import api


# 导入模型
from src.llm.model import model as llm_model

# 导入数据库服务
from src.persistent.db_history import history_service


class Service:

    def __init__(self):
        self.model_service = llm_model
        self.history_service = history_service


def main():


    app = Service()
    uvicorn.run(api.create_app(app),
                host="0.0.0.0",
                port=5200)

if __name__ == "__main__":
    main()
