from peewee import *
from langchain_core.messages import HumanMessage, AIMessage
from datetime import datetime
from langgraph.checkpoint.postgres import PostgresSaver
import logging
from persistent import yml

db = None
history_service = None

logger = logging.getLogger(__name__)

def init():
    global db, history_service
    db = PostgresqlDatabase(
        yml.all_yaml.get('database.db_name.long_term'),
        user=yml.all_yaml.get('database.user'),
        password=yml.all_yaml.get('database.password'),
        host=yml.all_yaml.get('database.host'),
        port=yml.all_yaml.get('database.port')
    )

    history_service = HistoryService()
    logger.info("数据库连接初始化")

"""
    长期对话历史记录模型
"""
class BaseModel(Model):
    class Meta:
        database = db

class ChatHistory(BaseModel):
    id = AutoField(primary_key=True)
    user_id = IntegerField(index=True)
    tag = CharField(null=True, index=True)
    information = TextField(null=False)

    class Meta:
        table_name = yml.all_yaml.get('database.table.long_term')
        indexes = (
            (('user_id', 'tag'), True),
        )

class HistoryService:

    def __init__(self):
        try:
            with db:
                db.create_tables([ChatHistory], safe=True)  # safe=True = 不存在才创建
            logger.info("✅ 长期对话历史记录数据库表初始化完成")
        except Exception as e:
            logger.error(f"初始化长期对话历史记录数据库表失败: {e}")

    """
        保存或更新长期对话历史记录
    """
    @staticmethod
    async def save_or_update_msg(user_id: int, tag: str, information: str):
        try:
            record, created = await ChatHistory.get_or_create(
                user_id=user_id,
                tag=tag,
                defaults={
                    "information": information,
                    "create_time": datetime.now()
                }
            )
            if not created:
                record.information = information
                record.update_time = datetime.now()
                await record.save()
            return record
        except Exception as e:
            logger.error(f"保存失败: {e}")
            return None

    """
        获取长期对话历史记录
    """
    @staticmethod
    async def get_history(user_id: int, limit: int = 10):
        try:
            records = await (
                ChatHistory.select()
                .where(ChatHistory.user_id == user_id)
                .order_by(ChatHistory.create_time.asc())
                .limit(limit)
            )

            history = []
            async for record in records:
                history.append(record.tag)
            return history
        except Exception as e:
            logger.error(f"获取长期对话历史记录失败: {e}")
            return []

    """
        获取指定用户的长期对话历史
    """
    @staticmethod
    async def get_history_by_tag(user_id: int, tag: str):
        try:
            record = await (
                ChatHistory.select().first()
                .where(ChatHistory.user_id == user_id)
                .where(ChatHistory.tag == tag)
            )
            return record
        except Exception as e:
            logger.error(f"获取长期对话历史记录失败: {e}")
            return None

    """
        获取用户的所有长期对话历史记录
    """
    @staticmethod
    async def get_all_history(user_id: int):
        try:
            records = await (
                ChatHistory.select()
                .where(ChatHistory.user_id == user_id)
            )
            history = {}
            async for record in records:
                history[record.tag] = record.information
            return history
        except Exception as e:
            logger.error(f"获取长期对话历史记录失败: {e}")
            return {}

    """
        清除长期对话历史记录
    """
    @staticmethod
    async def clear_history(user_id: int):
        try:
            await ChatHistory.delete().where(ChatHistory.user_id == user_id).execute()
            logger.info(f"✅ 长期对话历史记录清除成功: {user_id}")
        except Exception as e:
            logger.error(f"清除长期对话历史记录失败: {e}")

    @staticmethod
    async def get_history_count(user_id: int):
        try:
            return await ChatHistory.select().where(ChatHistory.user_id == user_id).count()
        except Exception as e:
            logger.error(f"获取长期对话历史记录数量失败: {e}")
            return 0

    @staticmethod
    def get_chat_history():
        return ChatHistory
