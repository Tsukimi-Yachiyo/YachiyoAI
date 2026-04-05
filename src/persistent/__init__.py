"""
    # 持久层
    包括 postgresSQL Redis 等数据库

"""

from .db_history import init as db_history_init
from .db_api_depository import init as api_depository_init

def init_db():
    db_history_init()
    api_depository_init()
