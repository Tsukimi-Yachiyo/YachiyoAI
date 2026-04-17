"""
API Key Mapper - 数据库模型定义
仅负责定义数据库表结构，不执行任何业务逻辑

注意：使用全局装饰器（通过 DLC embed 插件注入）
"""

# Mapper 装饰器已全局可用，无需 import
from peewee import AutoField, CharField, TextField, BooleanField, DateTimeField
from playhouse.migrate import SQL


@Mapper(table_name="api_keys")
class ApiKeyMapper:
    """API Key 数据库模型 - 只定义表结构"""
    id = AutoField()
    key = CharField(unique=True)
    name = CharField(null=True)
    description = TextField(null=True)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    updated_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
