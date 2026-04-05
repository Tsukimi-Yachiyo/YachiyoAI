from peewee import *
from langchain_core.messages import HumanMessage, AIMessage
from datetime import datetime
from langgraph.checkpoint.postgres import PostgresSaver
import logging, db_history
from persistent import yml

db = db_history.db
history_service = None

logger = logging.getLogger(__name__)

class ApiDepository(db_history.BaseModel):
    id = AutoField(primary_key=True)
    user_id = IntegerField(index=True,null=False)
    api_key = CharField(null=False)
    base_url = CharField(null=False)
    model = CharField(null=False)

    remain_tokens = IntegerField(null=False, default=100000)

    class Meta:
        table_name = yml.all_yaml.get('database.table.api_depository')
        indexes = (
            (('user_id', 'tag'), True),
        )

class ApiDepositoryService:

    def __init__(self):
        try:
            with db:
                db.create_tables([ApiDepository], safe=True)  # safe=True = 不存在才创建
            logger.info("✅ API仓库数据库表初始化完成")
        except Exception as e:
            logger.error(f"初始化API仓库数据库表失败: {e}")

    """
        保存或更新API仓库信息
    """
    @staticmethod
    async def save_or_update_msg(user_id: int, tag: str, information: str):
        try:
            record, created = await ApiDepository.get_or_create(
                api_key=information.api_key,
                base_url=information.base_url,
                model=information.model,
                remain_tokens=information.remain_tokens,
                defaults={
                    "remain_tokens": information.remain_tokens,
                    "create_time": datetime.now()
                }
            )
            if not created:
                record.remain_tokens = information.remain_tokens
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
