from peewee import *
from src.config import settings
from langchain_core.messages import HumanMessage, AIMessage
from datetime import datetime

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
    def save_msg(session_id: str, message: HumanMessage | AIMessage):
        ChatHistory.create(
            message_id=session_id,
            user=message.content,
            ai=message.content
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