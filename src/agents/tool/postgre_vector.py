from langchain_postgres import PGVector
from langchain.tools import tool
from persistent import yml
from llm import model
from config import settings

username = settings.DB_USER
password = settings.DB_PASSWORD
host = settings.DB_HOST
port = settings.DB_PORT
collection_name = settings.KNOWLEDGE_BASE_DB_TABLE_NAME

CONNECTION_STRING = f"postgresql+asyncpg://{username}:{password}@{host}:{port}"
embeddings = model.model_service.embeddings_model

vector_store = PGVector(embeddings=embeddings, collection_name=collection_name, connection=CONNECTION_STRING, async_mode=True)
max_retriever = vector_store.as_retriever(search_kwargs={"k": 5})
min_retriever = vector_store.as_retriever(search_kwargs={"k": 3})

async def max_retrieve_documents(query: str):
    """从 PostgreSQL 向量库检索相关内容，用于回答用户问题。
        从数据库中检索最多5个文档
    """
    retrieved_docs = await max_retriever.ainvoke(query)
    return retrieved_docs

async def min_retrieve_documents(query: str):
    """从 PostgreSQL 向量库检索相关内容，用于回答用户问题。
        从数据库中检索最多3个文档
    """
    retrieved_docs = await min_retriever.ainvoke(query)
    return retrieved_docs
