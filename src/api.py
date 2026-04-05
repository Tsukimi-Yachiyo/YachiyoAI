from fastapi import FastAPI


def create_app(service):

    app = FastAPI(title="YachiyoAI", version="2.0")

    """
        普通用户接口
    """

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.get("/chat")
    async def chat():
        result = await service.chat()
        return result

    @app.post("/add_api_key")
    async def add_api_key():
        return {"message": "Add API Key"}

    """
        获取配置
    """
    @app.get("/settings")
    async def settings():
        return {"settings": settings.model_config}

    return app