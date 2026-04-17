"""
LLM Service - 大语言模型服务
提供与大模型交互的功能，使用 API Key 进行认证

注意：Service、auto_inject 和 library 已通过 DLC embed 插件全局可用
"""

# Service 和 auto_inject 装饰器已全局可用，无需 import
import logging


logger = logging.getLogger(__name__)


def _log_info(msg):
    logging.getLogger(__name__).info(msg)


def _log_error(msg):
    logging.getLogger(__name__).error(msg)


def _log_warning(msg):
    logging.getLogger(__name__).warning(msg)


@Service
class LLMService:
    """大语言模型服务 - 提供 LLM 调用功能"""
    
    @auto_inject()
    def __init__(self, ApiKeyService: 'ApiKeyService'):
        self.api_key_service = ApiKeyService
        self.base_url = "https://api.openai.com/v1"
    
    def call_llm_with_retry(self, messages, max_retries=3):
        """调用大模型，带重试机制"""
        last_error = None
        
        for attempt in range(max_retries):
            api_key = self.api_key_service.get_available_api_key()
            
            if not api_key:
                _log_error("没有可用的 API Key")
                raise Exception("没有可用的 API Key")
            
            try:
                response = self._make_api_call(api_key, messages)
                _log_info(f"成功调用大模型，使用 Key: {api_key[:8]}...")
                return response
                
            except Exception as e:
                last_error = e
                _log_warning(f"API Key {api_key[:8]}... 调用失败: {e}")
                
                if self._is_key_invalid_error(e):
                    _log_warning(f"API Key {api_key[:8]}... 已失效，正在删除...")
                    self.api_key_service.remove_api_key(api_key)
                
                continue
        
        _log_error(f"调用大模型失败，已重试 {max_retries} 次")
        raise last_error
    
    def _make_api_call(self, api_key, messages):
        """实际的 API 调用方法"""
        # 模拟响应（实际使用时替换为真实的 API 调用）
        return {
            "choices": [{
                "message": {
                    "content": f"这是使用 API Key {api_key[:8]}... 的模拟响应"
                }
            }]
        }
    
    def _is_key_invalid_error(self, error):
        """判断错误是否由 API Key 无效引起"""
        error_str = str(error).lower()
        invalid_keywords = [
            "invalid api key",
            "unauthorized",
            "authentication failed",
            "api key expired",
            "401",
            "403"
        ]
        return any(keyword in error_str for keyword in invalid_keywords)
