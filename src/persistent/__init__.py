"""
    # 持久层
    包括 postgresSQL Redis 等数据库

"""

from .db_history import init as db_history_init

def init():
    db_history_init()
