import uvicorn
from playhouse.pwasyncio import await_

import api


# 导入模型
from src.llm.model import model as llm_model

# 导入数据库服务
from src.persistent.db_history import history_service

from agents import start
from persistent.json import json_init


class Service:

    def __init__(self):
        self.model_service = llm_model
        self.history_service = history_service
        self.agents = start.StartAgent(self.model_service.get_llm())
        self.state = self.agents.get_state()

        json_init()

    async def chat(self, prompt: str, conversationId: int):
        config = {"configurable": {"thread_id": conversationId}}
        result = await self.state.ainvoke(
            {"messages": [("user",prompt)]},
                config)
        return result["messages"][-1].content

    async def stream(self,prompt):
        # 以后添加流式输出
        pass

    def get_graph(self):
        self.agents.get_graph()

def main():

    app = Service()

    app.get_graph()
    uvicorn.run(api.create_app(app),
                host="0.0.0.0",
                port=5200)

if __name__ == "__main__":
    main()
