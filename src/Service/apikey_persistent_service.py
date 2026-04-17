"""
API Key Persistent Service - 持久化服务
仅负责 API Key 的数据库操作和内存缓存管理

注意：Service、auto_inject 和 library 已通过 DLC embed 插件全局可用
"""

# Service 和 auto_inject 装饰器已全局可用，无需 import
# library 变量也已全局可用
import logging
from datetime import datetime


logger = logging.getLogger(__name__)


def _log_info(msg):
    logging.getLogger(__name__).info(msg)


def _log_error(msg):
    logging.getLogger(__name__).error(msg)


def _log_warning(msg):
    logging.getLogger(__name__).warning(msg)


@Service
class ApiKeyPersistentService:
    """API Key 持久化服务 - 只负责数据库和内存缓存"""
    
    @auto_inject()
    def __init__(self):
        self.memory_cache = {}
        self._api_key_model = None
        self._cache_loaded = False
    
    @property
    def api_key_model(self):
        """获取 API Key 模型"""
        if self._api_key_model is None:
            # 使用全局 library 变量，无需 import
            self._api_key_model = library.dependencies["Mapper"]["ApiKeyMapper"]
        return self._api_key_model
    
    def _ensure_cache_loaded(self):
        """确保缓存已加载"""
        if not self._cache_loaded:
            self._load_active_keys_to_memory()
            self._cache_loaded = True
    
    def _load_active_keys_to_memory(self):
        """从数据库加载活跃 API Key 到内存"""
        try:
            model = self.api_key_model
            # 使用遍历方式避免 Peewee 字段访问问题
            all_keys = list(model.select())
            for key_obj in all_keys:
                # 确保是实例而不是字段描述符
                if hasattr(key_obj, 'key') and hasattr(key_obj, 'is_active'):
                    if key_obj.is_active == True:
                        self.memory_cache[key_obj.key] = key_obj
            _log_info(f"加载 {len(self.memory_cache)} 个 API Key 到缓存")
        except Exception as e:
            _log_error(f"加载 API Key 失败: {e}")
