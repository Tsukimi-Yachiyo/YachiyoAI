"""
API Key Service - API Key 管理服务
提供 API Key 的增删改查、生成和验证功能

注意：Service、auto_inject、save 和 library 已通过 DLC embed 插件全局可用
"""

# Service 和 auto_inject 装饰器已全局可用，无需 import
import logging
import random
import string
from datetime import datetime


logger = logging.getLogger(__name__)


def _log_info(msg):
    logging.getLogger(__name__).info(msg)


def _log_error(msg):
    logging.getLogger(__name__).error(msg)


def _log_warning(msg):
    logging.getLogger(__name__).warning(msg)


def _log_debug(msg):
    logging.getLogger(__name__).debug(msg)


@Service
class ApiKeyService:
    """API Key 管理服务 - 提供完整的 API Key 管理功能"""
    
    @auto_inject()
    def __init__(self, ApiKeyPersistentService: 'ApiKeyPersistentService'):
        self.persistence = ApiKeyPersistentService
    
    def generate_api_key(self, prefix="sk-", length=32):
        """生成随机 API Key"""
        characters = string.ascii_letters + string.digits
        random_part = ''.join(random.choice(characters) for _ in range(length))
        return f"{prefix}{random_part}"
    
    def add_api_key(self, name=None, description=None, key=None):
        """添加 API Key"""
        if key is None:
            key = self.generate_api_key()
        
        if key in self.persistence.memory_cache:
            raise ValueError(f"API Key '{key}' 已存在")
        
        try:
            api_key_obj = save(
                self.persistence.api_key_model,
                key=key,
                name=name,
                description=description,
                is_active=True
            )
            self.persistence.memory_cache[key] = api_key_obj
            _log_info(f"添加 API Key: {key[:8]}...")
            return api_key_obj
        except Exception as e:
            _log_error(f"添加 API Key 失败: {e}")
            raise
    
    def remove_api_key(self, key):
        """从内存和数据库中删除 API Key"""
        if key in self.persistence.memory_cache:
            del self.persistence.memory_cache[key]
        
        try:
            for record in self.persistence.api_key_model.select():
                if record.key == key:
                    record.delete_instance()
                    _log_info(f"删除 API Key: {key[:8]}...")
                    return True
            _log_warning(f"未找到 API Key: {key[:8]}...")
            return False
        except Exception as e:
            _log_error(f"删除 API Key 失败: {e}")
            raise
    
    def deactivate_api_key(self, key):
        """停用 API Key（软删除）"""
        if key in self.persistence.memory_cache:
            del self.persistence.memory_cache[key]
        
        try:
            for record in self.persistence.api_key_model.select():
                if record.key == key:
                    record.is_active = False
                    record.updated_at = datetime.now()
                    record.save()
                    _log_info(f"停用 API Key: {key[:8]}...")
                    return True
            _log_warning(f"未找到 API Key: {key[:8]}...")
            return False
        except Exception as e:
            _log_error(f"停用 API Key 失败: {e}")
            raise
    
    def get_available_api_key(self):
        """获取一个可用的 API Key"""
        self.persistence._ensure_cache_loaded()
        if not self.persistence.memory_cache:
            _log_warning("没有可用的 API Key")
            return None
        
        available_keys = list(self.persistence.memory_cache.keys())
        selected_key = random.choice(available_keys)
        _log_debug(f"选择 API Key: {selected_key[:8]}...")
        return selected_key
    
    def validate_api_key(self, key):
        """验证 API Key 是否有效"""
        self.persistence._ensure_cache_loaded()
        return key in self.persistence.memory_cache
    
    def list_all_api_keys(self, include_inactive=False):
        """列出所有 API Key"""
        if include_inactive:
            return list(self.persistence.api_key_model.select())
        else:
            return [key_obj for key_obj in self.persistence.memory_cache.values()]
    
    def get_api_key_info(self, key):
        """获取 API Key 的详细信息"""
        return self.persistence.memory_cache.get(key)
