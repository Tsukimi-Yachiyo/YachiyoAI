from fastapi import FastAPI


def create_app(service):

    app = FastAPI(title="YachiyoAI", version="2.0")

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.get("/chat")
    async def chat():
        return {"message": "Chat"}

    @app.post("/add_api_key")
    async def add_api_key():
        return {"message": "Add API Key"}

    return app