import uvicorn
from playhouse.pwasyncio import await_

import api


# 导入模型
from llm.model import model_init
from llm import model

# 导入数据库服务
from persistent.db_history import history_service
from persistent import init as db_init

from agents import start
from persistent.json import json_init
from persistent.yml import yaml_init
from persistent import yml
from tool.logging import logging_init

"""
    服务模块
    包括模型服务
    包括数据库服务
    包括智能体服务
"""
class Service:

    def __init__(self):
        # 初始化
        logging_init()
        yaml_init()
        json_init()
        model_init()
        db_init()

        # 初始化服务
        self.model_service = model.model_service
        self.history_service = history_service
        self.agents = start.StartAgent(self.model_service.get_llm())
        self.state = self.agents.get_state()

    """
        聊天服务
        :param prompt: 用户输入
        :param conversationId: 会话ID
        :return: 模型回复
    """
    async def chat(self, prompt: str, conversationId: int):
        config = {"configurable": {"thread_id": conversationId}}
        result = await self.state.ainvoke(
            {"messages": [("user",prompt)]},
                config)
        return result["messages"][-1].content

    async def stream(self,prompt):
        # 以后添加流式输出
        pass

    """
        绘制状态图
    """
    def get_graph(self):
        self.agents.get_graph()

"""
   主函数
"""
def main():

    app = Service()

    # app.get_graph()
    """
        启动API服务
    """
    uvicorn.run(api.create_app(app),
                host="0.0.0.0",
                port=5200)

if __name__ == "__main__":
    main()
