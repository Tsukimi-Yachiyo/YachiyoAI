from peewee import *
from src.config import settings
from langchain_core.messages import HumanMessage, AIMessage
from datetime import datetime
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg.rows import dict_row

db = PostgresqlDatabase(
    settings.DB_NAME,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT
)

"""
    对话历史记录模型
"""

pool = ConnectionPool(
    # 关键修复：用真实配置拼接连接字符串
    conninfo=f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
    configure=db,
    max_size=60,
    kwargs={"autocommit": True, "row_factory": dict_row}
)

class BaseModel(Model):
    class Meta:
        database = db

class ChatHistory(BaseModel):
    message_id = TextField(null=False)  # 对话会话ID
    user = TextField(null=False)  # 用户内容
    ai = TextField(null=False)  # 模型回复内容
    create_time = DateTimeField(default=datetime.now)  # 时间

    class Meta:
        table_name = "chat_history"

class HistoryService:

    def __init__(self):
        with db:
            db.create_tables([ChatHistory], safe=True)  # safe=True = 不存在才创建
        print("✅ Peewee 数据库表初始化完成")

    """
        保存对话历史
    """
    @staticmethod
    def save_msg(session_id: str, ai_message: AIMessage, human_message: HumanMessage):
        ChatHistory.create(
            message_id=session_id,
            user=human_message.user,
            ai=human_message.ai,
        )

    """
        获取对话历史
    """
    @staticmethod
    def get_history(session_id: str, limit: int = 10):
        records = (
            ChatHistory.select()
            .where(ChatHistory.message_id == session_id)
            .order_by(ChatHistory.create_time.asc())
            .limit(limit)
        )

        messages = []
        for record in records:
            messages.append(HumanMessage(content=record.user))
            messages.append(AIMessage(content=record.ai))
        return messages

    @staticmethod
    def clear_history(session_id: str):
        ChatHistory.delete().where(ChatHistory.message_id == session_id).execute()

    @staticmethod
    def get_history_count(session_id: str):
        return ChatHistory.select().where(ChatHistory.message_id == session_id).count()

    @staticmethod
    def get_chat_history():
        return ChatHistory

history_service = HistoryService()