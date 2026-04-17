"""
API Key 请求模型定义
使用 @Struct 装饰器注册到全局命名空间
解决跨模块访问问题
"""

from pydantic import BaseModel
from typing import Optional


@Struct
class AddApiKeyRequest(BaseModel):
    """添加 API Key 请求模型"""
    name: Optional[str] = None
    description: Optional[str] = None
    key: Optional[str] = None


@Struct
class RemoveApiKeyRequest(BaseModel):
    """删除/停用 API Key 请求模型"""
    key: str
